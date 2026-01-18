from session import TrainingSession

class Runner:
    """
    Represents one runner and their session history.
    """

    def __init__(self, name: str, age: int, level: str):
        self.name = name
        self.age = int(age)
        self.level = level
        self.sessions: list[TrainingSession] = []

    def add_session(self, session: TrainingSession):
        self.sessions.append(session)

    def total_distance(self) -> float:
        return sum(s.distance_km for s in self.sessions)

    def average_pace(self) -> float:
        total_dist = self.total_distance()
        if total_dist <= 0:
            return 0.0
        total_time = sum(s.duration_min for s in self.sessions)
        return total_time / total_dist

    def total_load(self) -> float:
        # Polymorphism in action: calculate_load differs by session type
        return sum(s.calculate_load() for s in self.sessions)


