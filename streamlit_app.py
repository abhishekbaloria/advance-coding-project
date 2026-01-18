import streamlit as st

from runner import Runner
from session import TrainingSession, IntervalSession
from plan import TrainingPlan
from storage_json import save_sessions_to_json, load_sessions_from_json
from storage_sqlite import init_db, insert_session, load_sessions_from_db

# ---------- APP SETUP ----------
st.set_page_config(page_title="Running Training Planner", layout="centered")
st.title("🏃‍♂️ Running Training Planner")
st.write("Log your runs, track stats, and plan training sessions.")

# ---------- INIT ----------
if "runner" not in st.session_state:
    runner = Runner("Abhishek", 22, "Beginner")
    init_db()

    db_sessions = load_sessions_from_db()
    if db_sessions:
        runner.sessions = db_sessions
    else:
        runner.sessions = load_sessions_from_json()

    st.session_state.runner = runner

runner = st.session_state.runner

# ---------- ADD SESSION ----------
st.header("➕ Add Training Session")

distance = st.number_input("Distance (km)", min_value=0.0, step=0.1)
duration = st.number_input("Duration (minutes)", min_value=0.0, step=1.0)
session_type = st.selectbox("Session Type", ["Normal Run", "Interval Run"])

intervals = 0
if session_type == "Interval Run":
    intervals = st.number_input("Intervals", min_value=1, step=1)

if st.button("Add Session"):
    if session_type == "Normal Run":
        session = TrainingSession(distance, duration)
    else:
        session = IntervalSession(distance, duration, intervals)

    runner.add_session(session)
    insert_session(session)
    save_sessions_to_json(runner.sessions)

    st.success("Session added successfully!")

# ---------- STATS ----------
st.markdown("---")
st.header("📊 Your Stats")

st.write(f"**Total Distance:** {runner.total_distance():.2f} km")
st.write(f"**Average Pace:** {runner.average_pace():.2f} min/km")
st.write(f"**Training Load:** {runner.total_load():.2f}")

# ---------- HISTORY ----------
st.markdown("---")
st.header("📁 Training History")

if not runner.sessions:
    st.write("No sessions added yet.")
else:
    for i, s in enumerate(runner.sessions, 1):
        st.write(
            f"{i}. {s.__class__.__name__} | "
            f"{s.distance_km} km | "
            f"{s.duration_min} min | "
            f"Load: {s.calculate_load():.2f}"
        )

# ---------- PLAN ----------
st.markdown("---")
st.header("📅 Weekly Training Plan")

tp = TrainingPlan(runner.level)
plan = tp.generate_week()

for day in plan:
    st.write(f"- {day}")
