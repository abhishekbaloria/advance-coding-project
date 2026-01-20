# importing the Runner class which represents the user (runner)
# and TrainingSession / IntervalSession which represent different run types
from runner import Runner
from session import TrainingSession, IntervalSession


# this function just prints the menu options on the terminal
# it helps keep the code clean instead of repeating print statements
def show_menu():
    print("\nRunning Training Planner")
    print("1. Add normal training session")
    print("2. Add interval training session")
    print("3. View training history")
    print("4. Exit")


# this is the main function where the program actually runs
def main():

    # creating a Runner object
    # name, age and level are passed when the program starts
    runner = Runner("Abhishek", 22, "Beginner")

    # infinite loop so the menu keeps showing until user exits
    while True:
        show_menu()

        # taking user input to decide what action to perform
        choice = input("Choose an option: ")

        # option 1 → normal training session
        if choice == "1":
            distance = float(input("Distance (km): "))
            duration = float(input("Duration (minutes): "))

            # creating a TrainingSession object
            session = TrainingSession(distance, duration)

            # adding session to runner history
            runner.add_session(session)
            print("Training session added.")

        # option 2 → interval training session
        elif choice == "2":
            distance = float(input("Distance (km): "))
            duration = float(input("Duration (minutes): "))
            intervals = int(input("Number of intervals: "))

            # creating an IntervalSession object
            session = IntervalSession(distance, duration, intervals)

            # adding interval session to runner history
            runner.add_session(session)
            print("Interval session added.")

        # option 3 → show all stored sessions
        elif choice == "3":
            runner.show_sessions()

        # option 4 → exit the program
        elif choice == "4":
            print("See you on your next run 🏃‍♂️")
            break

        # handles invalid inputs
        else:
            print("Invalid choice. Please try again.")


# this makes sure main() only runs when this file is executed directly
if __name__ == "__main__":
    main()
