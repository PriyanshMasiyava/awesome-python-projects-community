student = {}

while True:
    print("\n--------- STUDENT MANAGER APP ---------")
    print("1. Add Student")
    print("2. View Student")
    print("3. Check Result")
    print("4. Exit")

    choice = input("Enter your choice: ")

    # Add Student
    if choice == "1":
        name = input("Enter Student Name: ")
        marks = int(input("Enter Marks: "))
        student[name] = marks
        print(f"{name} Successfully Added!")

    # View Student
    elif choice == "2":
        if not student:
            print("No Student Found!")
        else:
            print("\nStudent List:")
            for name, marks in student.items():
                print(f"{name} : {marks}")

    # Check Result
    elif choice == "3":
        name = input("Enter Student Name: ")

        if name in student:
            marks = student[name]

            if marks >= 40:
                print(f"{name} is Pass.")
            else:
                print(f"{name} is Fail.")
        else:
            print("Student Not Found!")

    # Exit
    elif choice == "4":
        print("Exiting...")
        break

    # Invalid Choice
    else:
        print("Invalid Input! Please enter 1, 2, 3, or 4.")