# Advanced-Coding-Running-Training-Planner
Python application inspired by my recent interest in running, designed to help runners plan training schedules, track runs, and analyze progress.
---
## Running Training Planner (Strava-Style)
This is a simple running training planner made using Streamlit.
You can log your runs, view basic stats, see graphs (distance/pace/load), and get a basic weekly training plan.

## Features
Add Runs: Log distance, duration, date, and run type

Normal + Interval Runs: Interval runs include number of intervals

Quick Stats: Total km, average pace, total load, total runs

Filters: Filter by date range and session type

Graphs (Strava-style basics): Distance, pace, load, weekly distance

Training Plan: Auto weekly plan based on runner level

Data Persistence: Saves runs using SQLite + JSON

# How to Run
Install Streamlit (and other requirements)
```bash 
pip install -r requirements.txt
   ```
Save the Code
Keep all files inside the same folder (don’t remove data/ or JSON files).
Run the App
Open terminal, go to the project folder, then run:
```bash
  streamlit run streamlit_app.py
  ```

## Gameplay (How to Use)
Add a Run: Fill in date, distance, duration, and type → click Save Run

Interval Runs: If you choose interval, also enter intervals

Filters: Pick session types + date range to see only the runs you want

Graphs: Choose a graph from the dropdown to view trends

Weekly Plan: Scroll down to see the weekly plan suggestions

Game Mechanics (App Logic)

Distance (km): Total km for the run

Duration (min): Total minutes for the run

Pace (min/km): Duration ÷ distance

Training Load: Simple training load based on session type (intervals = higher load)

Persistence: Runs are stored in SQLite and also backed up in JSON

## Future Enhancements

Add heart-rate / effort based load

More advanced weekly plan (goal-based)

Personal best detection (5K / 10K etc.)

Export to CSV

Better UI (more Strava-like design)


