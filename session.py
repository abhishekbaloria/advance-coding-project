import datetime


class TrainingSession:
    """
    Base class for a running session.
    Demonstrates inheritance + polymorphism via calculate_load().
    """

    def __init__(self, distance_km: float, duration_min: float, session_date=None):
        self.distance_km = float(distance_km)
        self.duration_min = float(duration_min)

        # if date not given, save today's date
        if session_date is None:
            self.session_date = datetime.date.today().isoformat()
        else:
            self.session_date = str(session_date)

    def pace_min_per_km(self) -> float:
        if self.distance_km <= 0:
            return 0.0
        return self.duration_min / self.distance_km

    def calculate_load(self) -> float:
        # simple base load (can be improved later)
        return self.distance_km

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "distance_km": self.distance_km,
            "duration_min": self.duration_min,
            "session_date": self.session_date
        }

    @staticmethod
    def from_dict(data: dict):
        t = data.get("type", "TrainingSession")

        # if old data doesn't have date, it will use today's date
        d = data.get("session_date", None)

        if t == "IntervalSession":
            return IntervalSession(
                data["distance_km"],
                data["duration_min"],
                data.get("intervals", 0),
                d
            )

        return TrainingSession(data["distance_km"], data["duration_min"], d)


class IntervalSession(TrainingSession):
    def __init__(self, distance_km: float, duration_min: float, intervals: int, session_date=None):
        super().__init__(distance_km, duration_min, session_date)
        self.intervals = int(intervals)

    def calculate_load(self) -> float:
        # a bit higher load for interval sessions
        return super().calculate_load() * 1.2

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["intervals"] = self.intervals
        return base

