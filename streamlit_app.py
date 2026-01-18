import streamlit as st
import pandas as pd
import datetime

# try to import matplotlib, otherwise fall back to streamlit charts
try:
    import importlib
    plt = importlib.import_module("matplotlib.pyplot")
    HAVE_MPL = True
except Exception:
    plt = None
    HAVE_MPL = False

from runner import Runner
from session import TrainingSession, IntervalSession
from plan import TrainingPlan
from storage_json import save_sessions_to_json, load_sessions_from_json
from storage_sqlite import init_db, insert_session, load_sessions_from_db


# basic page stuff
st.set_page_config(page_title="Running Training Planner", layout="wide")
st.title("🏃‍♂️ Running Training Planner")
st.write("A basic Strava-like tracker for runs (made for my advanced coding project).")


# runner should not reset on every click so we keep it in session_state
if "runner_data" not in st.session_state:
    temp_runner = Runner("Abhishek", 22, "Beginner")

    init_db()  # make db table if it doesn't exist

    # try loading from database first, if empty then use json
    from_db = load_sessions_from_db()
    if from_db:
        temp_runner.sessions = from_db
    else:
        temp_runner.sessions = load_sessions_from_json()

    st.session_state.runner_data = temp_runner

runner = st.session_state.runner_data


# ---------------- ADD RUN ----------------
st.markdown("---")
st.header("➕ Add a Run")

c1, c2, c3, c4 = st.columns(4)

with c1:
    run_date = st.date_input("Date", value=datetime.date.today())

with c2:
    dist = st.number_input("Distance (km)", min_value=0.0, step=0.1)

with c3:
    dur = st.number_input("Duration (min)", min_value=0.0, step=1.0)

with c4:
    run_type = st.selectbox("Type", ["Normal", "Interval"])

intervals = 0
if run_type == "Interval":
    intervals = st.number_input("Intervals", min_value=1, step=1)

if st.button("Save Run"):
    date_text = run_date.isoformat()

    if run_type == "Normal":
        new_run = TrainingSession(dist, dur, date_text)
    else:
        new_run = IntervalSession(dist, dur, intervals, date_text)

    runner.add_session(new_run)

    # save both (course requirement)
    insert_session(new_run)
    save_sessions_to_json(runner.sessions)

    st.success("Saved ✅")


# ---------------- MAKE DATAFRAME ----------------
runs = []
for s in runner.sessions:
    runs.append({
        "date": getattr(s, "session_date", None),
        "type": s.__class__.__name__,
        "distance_km": s.distance_km,
        "duration_min": s.duration_min,
        "pace_min_km": round(s.pace_min_per_km(), 2),
        "load": round(s.calculate_load(), 2),
        "intervals": getattr(s, "intervals", 0)
    })

df = pd.DataFrame(runs)

st.markdown("---")
st.header("🎛️ Filters")

if df.empty:
    st.info("No runs saved yet. Add one above.")
    st.stop()

# convert date column safely (if something is missing, make it today's date)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# if any date is invalid/missing -> NaT, fill it with today
df["date"] = df["date"].fillna(pd.Timestamp.today())

df = df.sort_values("date")



# filters
f1, f2, f3 = st.columns(3)

with f1:
    all_types = sorted(df["type"].unique())
    picked_types = st.multiselect("Session types", all_types, default=all_types)

with f2:
    min_d = df["date"].dropna().min().date()
max_d = df["date"].dropna().max().date()

drange = st.date_input("Date range", (min_d, max_d))


with f3:
    show_table = st.checkbox("Show table", value=True)

start_d, end_d = drange

df_f = df[
    (df["type"].isin(picked_types)) &
    (df["date"].dt.date >= start_d) &
    (df["date"].dt.date <= end_d)
].copy()


# ---------------- STATS ----------------
st.markdown("---")
st.header("📊 Quick Stats")

x1, x2, x3, x4 = st.columns(4)
x1.metric("Runs", len(df_f))
x2.metric("Total km", f"{df_f['distance_km'].sum():.2f}")

if df_f["distance_km"].sum() > 0:
    avg_pace = df_f["duration_min"].sum() / df_f["distance_km"].sum()
else:
    avg_pace = 0

x3.metric("Avg pace", f"{avg_pace:.2f} min/km")
x4.metric("Total load", f"{df_f['load'].sum():.2f}")


# ---------------- TABLE ----------------
if show_table:
    st.markdown("---")
    st.header("📁 Run History")
    st.dataframe(df_f, use_container_width=True)


# ---------------- GRAPHS ----------------
st.markdown("---")
st.header("📈 Graphs")

graph = st.selectbox(
    "Pick a graph",
    ["Distance over time", "Pace over time", "Training load over time", "Weekly distance"]
)

if HAVE_MPL:
    fig, ax = plt.subplots()

    if graph == "Distance over time":
        ax.plot(df_f["date"], df_f["distance_km"])
        ax.set_ylabel("km")

    elif graph == "Pace over time":
        ax.plot(df_f["date"], df_f["pace_min_km"])
        ax.set_ylabel("min/km")

    elif graph == "Training load over time":
        ax.plot(df_f["date"], df_f["load"])
        ax.set_ylabel("load")

    else:
        weekly = df_f.set_index("date")["distance_km"].resample("W").sum()
        ax.plot(weekly.index, weekly.values)
        ax.set_ylabel("km per week")

    ax.set_xlabel("date")
    ax.tick_params(axis="x", rotation=25)
    st.pyplot(fig)
else:
    # fallback to Streamlit's native charting when matplotlib isn't installed
    if graph == "Distance over time":
        st.line_chart(df_f.set_index("date")["distance_km"])
    elif graph == "Pace over time":
        st.line_chart(df_f.set_index("date")["pace_min_km"])
    elif graph == "Training load over time":
        st.line_chart(df_f.set_index("date")["load"])
    else:
        weekly = df_f.set_index("date")["distance_km"].resample("W").sum()
        st.line_chart(weekly)


# ---------------- PLAN ----------------
st.markdown("---")
st.header("📅 Weekly Training Plan")

weekly_plan = TrainingPlan(runner.level).generate_week()
for line in weekly_plan:
    st.write("-", line)
