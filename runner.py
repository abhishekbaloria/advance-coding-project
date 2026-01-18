from session import TrainingSession

class Runner:
    """
    Represents a runner using the training planner.
    """

    def __init__(self, name, age, level):
        self.name = name
        self.age = age
        self.level = level
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def show_sessions(self):
        if not self.sessions:
            print("No training sessions yet.")
            return

        print("\nTraining History:")
        print("------------------")
        for i, session in enumerate(self.sessions, start=1):
            print(f"\nSession {i}")
            session.display_session()

