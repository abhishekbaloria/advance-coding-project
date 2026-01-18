class TrainingSession:
    """
    Base class for a running session.
    Demonstrates inheritance + polymorphism via calculate_load().
    """

    def __init__(self, distance_km: float, duration_min: float):
        self.distance_km = float(distance_km)
        self.duration_min = float(duration_min)

    def pace_min_per_km(self) -> float:
        if self.distance_km <= 0:
            return 0.0
        return self.duration_min / self.distance_km

    def calculate_load(self) -> float:
        """
        Polymorphic method:
        Child classes override this to calculate training load differently.
        """
        return self.distance_km  # basic load

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "distance_km": self.distance_km,
            "duration_min": self.duration_min
        }

    @staticmethod
    def from_dict(data: dict):
        t = data.get("type", "TrainingSession")
        if t == "IntervalSession":
            return IntervalSession(
                data["distance_km"],
                data["duration_min"],
                data.get("intervals", 0)
            )
        return TrainingSession(data["distance_km"], data["duration_min"])


class IntervalSession(TrainingSession):
    """
    Inherits from TrainingSession.
    Adds intervals and overrides calculate_load() (polymorphism).
    """

    def __init__(self, distance_km: float, duration_min: float, intervals: int):
        super().__init__(distance_km, duration_min)
        self.intervals = int(intervals)

    def calculate_load(self) -> float:
        # intervals increase intensity
        return self.distance_km + (self.intervals * 0.5)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["intervals"] = self.intervals
        return base
