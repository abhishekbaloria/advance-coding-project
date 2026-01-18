from flask import Flask, render_template, request
from runner import Runner
from session import TrainingSession, IntervalSession
from plan import TrainingPlan
from storage_json import save_sessions_to_json, load_sessions_from_json
from storage_sqlite import init_db, insert_session, load_sessions_from_db

app = Flask(__name__)

runner = Runner("Abhishek", 22, "Beginner")

# Initialize DB and load previous sessions (DB preferred, fallback JSON)
init_db()
db_sessions = load_sessions_from_db()
if db_sessions:
    runner.sessions = db_sessions
else:
    runner.sessions = load_sessions_from_json()

def build_stats():
    return {
        "total_distance": round(runner.total_distance(), 2),
        "avg_pace": round(runner.average_pace(), 2),
        "total_load": round(runner.total_load(), 2),
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        distance = float(request.form["distance"])
        duration = float(request.form["duration"])
        session_type = request.form["type"]

        if session_type == "normal":
            session = TrainingSession(distance, duration)
        else:
            intervals = int(request.form.get("intervals", 0) or 0)
            session = IntervalSession(distance, duration, intervals)

        runner.add_session(session)

        # persist to BOTH JSON + SQLite (covers assignment topics)
        insert_session(session)
        save_sessions_to_json(runner.sessions)

    return render_template("index.html", sessions=runner.sessions, stats=build_stats())

@app.route("/plan")
def plan():
    tp = TrainingPlan(runner.level)
    return render_template("plan.html", plan=tp.generate_week())

if __name__ == "__main__":
    app.run(debug=True)

