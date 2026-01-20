from runner import Runner
from session import TrainingSession

def show_menu():
    print("\nRunning Training Planner")
    print("1. Add training session")
    print("2. View training history")
    print("3. Exit")

def main():
    runner = Runner("Abhishek", 22, "Beginner")

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            distance = float(input("Enter distance (km): "))
            duration = float(input("Enter duration (minutes): "))
            session = TrainingSession(distance, duration)
            runner.add_session(session)
            print("Training session added.")

        elif choice == "2":
            runner.show_sessions()

        elif choice == "3":
            print("Good luck with your runs!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
from runner import Runner
from session import TrainingSession, IntervalSession

def show_menu():
    print("\nRunning Training Planner")
    print("1. Add normal training session")
    print("2. Add interval training session")
    print("3. View training history")
    print("4. Exit")

def main():
    runner = Runner("Abhishek", 22, "Beginner")

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            distance = float(input("Distance (km): "))
            duration = float(input("Duration (minutes): "))
            session = TrainingSession(distance, duration)
            runner.add_session(session)
            print("Training session added.")

        elif choice == "2":
            distance = float(input("Distance (km): "))
            duration = float(input("Duration (minutes): "))
            intervals = int(input("Number of intervals: "))
            session = IntervalSession(distance, duration, intervals)
            runner.add_session(session)
            print("Interval session added.")

        elif choice == "3":
            runner.show_sessions()

        elif choice == "4":
            print("See you on your next run 🏃‍♂️")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

