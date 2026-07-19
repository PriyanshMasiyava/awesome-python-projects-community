"""
====================================================
Project Name : Smart Calculator
Author       : Priyansh Masiyava
Version      : 1.0
Description  : A menu-driven calculator that performs
               basic arithmetic operations with
               proper input validation.
====================================================
"""

import math


class SmartCalculator:
    """A simple smart calculator with multiple arithmetic operations."""

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

    @staticmethod
    def modulus(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot perform modulus by zero.")
        return a % b

    @staticmethod
    def floor_division(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot perform floor division by zero.")
        return a // b

    @staticmethod
    def power(a, b):
        return a ** b

    @staticmethod
    def square_root(a):
        if a < 0:
            raise ValueError("Square root of a negative number is not possible.")
        return math.sqrt(a)

    @staticmethod
    def percentage(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot calculate percentage with zero.")
        return (a / b) * 100


def get_number(message):
    """Safely get a numeric input from the user."""
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.\n")


def display_menu():
    print("\n" + "=" * 45)
    print("          SMART CALCULATOR")
    print("=" * 45)
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Floor Division")
    print("7. Power")
    print("8. Square Root")
    print("9. Percentage")
    print("10. Clear Screen")
    print("0. Exit")
    print("=" * 45)


def main():
    calculator = SmartCalculator()

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                a = get_number("Enter First Number: ")
                b = get_number("Enter Second Number: ")
                print(f"✅ Result = {calculator.add(a, b)}")

            elif choice == "2":
                a = get_number("Enter First Number: ")
                b = get_number("Enter Second Number: ")
                print(f"✅ Result = {calculator.subtract(a, b)}")

            elif choice == "3":
                a = get_number("Enter First Number: ")
                b = get_number("Enter Second Number: ")
                print(f"✅ Result = {calculator.multiply(a, b)}")

            elif choice == "4":
                a = get_number("Enter First Number: ")
                b = get_number("Enter Second Number: ")
                print(f"✅ Result = {calculator.divide(a, b)}")

            elif choice == "5":
                a = get_number("Enter First Number: ")
                b = get_number("Enter Second Number: ")
                print(f"✅ Result = {calculator.modulus(a, b)}")

            elif choice == "6":
                a = get_number("Enter First Number: ")
                b = get_number("Enter Second Number: ")
                print(f"✅ Result = {calculator.floor_division(a, b)}")

            elif choice == "7":
                a = get_number("Enter Base Number: ")
                b = get_number("Enter Power: ")
                print(f"✅ Result = {calculator.power(a, b)}")

            elif choice == "8":
                a = get_number("Enter Number: ")
                print(f"✅ Result = {calculator.square_root(a)}")

            elif choice == "9":
                a = get_number("Enter Obtained Value: ")
                b = get_number("Enter Total Value: ")
                print(f"✅ Percentage = {calculator.percentage(a, b):.2f}%")

            elif choice == "10":
                print("\n" * 100)

            elif choice == "0":
                print("\nThank you for using Smart Calculator!")
                break

            else:
                print("❌ Invalid choice. Please select a valid option.")

        except Exception as error:
            print(f"❌ Error: {error}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()