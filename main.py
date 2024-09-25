import os


def run_script():
    while True:
        # Display menu options
        print("\nMain Menu:")
        print("1. Capture faces (capture.py)")
        print("2. Train model (train.py)")
        print("3. Take attendance (take_attendance.py)")
        print("q. Quit")

        # Get user's choice
        choice = input("Enter your choice (1/2/3 or 'q' to quit): ").strip().lower()

        # Execute the corresponding script based on user input
        if choice == '1':
            os.system('python capture.py')
        elif choice == '2':
            os.system('python train.py')
        elif choice == '3':
            os.system('python take_attendance.py')
        elif choice == 'q':
            print("Exiting the program.")
            break  # Exit the loop to quit the program
        else:
            print("Invalid choice. Please select 1, 2, 3, or 'q' to quit.")


if __name__ == "__main__":
    run_script()
