class TrainingSession:
    """
    Represents a single running training session.
    """

    def __init__(self, distance_km, duration_min):
        self.distance_km = distance_km
        self.duration_min = duration_min

    def calculate_pace(self):
        """
        Calculates pace in minutes per kilometer.
        """
        return self.duration_min / self.distance_km

    def display_session(self):
        pace = self.calculate_pace()
        print(f"Distance: {self.distance_km} km")
        print(f"Duration: {self.duration_min} min")
        print(f"Pace: {pace:.2f} min/km")
class TrainingSession:
    """
    Represents a basic running training session.
    """

    def __init__(self, distance_km, duration_min):
        self.distance_km = distance_km
        self.duration_min = duration_min

    def calculate_pace(self):
        return self.duration_min / self.distance_km

    def display_session(self):
        pace = self.calculate_pace()
        print(f"Distance: {self.distance_km} km")
        print(f"Duration: {self.duration_min} min")
        print(f"Pace: {pace:.2f} min/km")


class IntervalSession(TrainingSession):
    """
    Represents an interval training session (inherits from TrainingSession).
    """

    def __init__(self, distance_km, duration_min, intervals):
        super().__init__(distance_km, duration_min)
        self.intervals = intervals

    def display_session(self):
        super().display_session()
        print(f"Intervals: {self.intervals}")
