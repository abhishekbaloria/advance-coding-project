class TrainingPlan:
    """
    Generates a simple weekly plan based on runner level.
    """

    def __init__(self, level: str):
        self.level = level

    def generate_week(self) -> list[str]:
        if self.level == "Beginner":
            return [
                "Mon: Easy 3 km",
                "Wed: Easy 4 km",
                "Sat: Long run 5 km"
            ]
        if self.level == "Intermediate":
            return [
                "Mon: Easy 5 km",
                "Wed: Tempo 6 km",
                "Fri: Easy 4 km",
                "Sun: Long run 8 km"
            ]
        return [
            "Mon: Easy 8 km",
            "Tue: Intervals",
            "Thu: Tempo 10 km",
            "Sat: Easy 6 km",
            "Sun: Long run 15 km"
        ]

