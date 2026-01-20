import os
import sqlite3
from session import TrainingSession, IntervalSession


# returns the path to the database file
# also makes sure the data folder exists
def get_db_path() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "runs.db")


# creates the database and table if they do not already exist
def init_db():
    db = get_db_path()
    with sqlite3.connect(db) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                distance_km REAL NOT NULL,
                duration_min REAL NOT NULL,
                intervals INTEGER
            )
        """)
        conn.commit()


# saves one training session to the database
def insert_session(session: TrainingSession):
    db = get_db_path()
    with sqlite3.connect(db) as conn:

        # interval sessions store interval count
        if isinstance(session, IntervalSession):
            conn.execute(
                "INSERT INTO sessions (type, distance_km, duration_min, intervals) VALUES (?, ?, ?, ?)",
                (
                    session.__class__.__name__,
                    session.distance_km,
                    session.duration_min,
                    session.intervals
                )
            )

        # normal training sessions do not have intervals
        else:
            conn.execute(
                "INSERT INTO sessions (type, distance_km, duration_min, intervals) VALUES (?, ?, ?, ?)",
                (
                    session.__class__.__name__,
                    session.distance_km,
                    session.duration_min,
                    None
                )
            )

        conn.commit()


# loads all saved sessions from the database
# and converts them back into objects
def load_sessions_from_db() -> list[TrainingSession]:
    db = get_db_path()

    # if database does not exist, return empty list
    if not os.path.exists(db):
        return []

    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            "SELECT type, distance_km, duration_min, intervals FROM sessions ORDER BY id ASC"
        ).fetchall()

    sessions: list[TrainingSession] = []

    for t, dist, dur, inter in rows:
        if t == "IntervalSession":
            sessions.append(IntervalSession(dist, dur, inter or 0))
        else:
            sessions.append(TrainingSession(dist, dur))

    return sessions
