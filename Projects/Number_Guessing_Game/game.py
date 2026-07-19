"""
====================================================
Project Name : Number Guessing Game
Author       : Priyansh Masiyava
Version      : 1.0
Description  : Guess the secret number with
               multiple difficulty levels and
               high score tracking.
====================================================
"""

import json
import random
import os


class NumberGuessingGame:

    HIGH_SCORE_FILE = "highscore.json"

    def __init__(self):
        self.secret_number = 0
        self.max_attempts = 0
        self.score = 0

    def load_high_score(self):
        """Load high score from JSON file."""
        if not os.path.exists(self.HIGH_SCORE_FILE):
            return 0

        with open(self.HIGH_SCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)

    def save_high_score(self, score):
        """Save new high score."""
        with open(self.HIGH_SCORE_FILE, "w") as file:
            json.dump({"high_score": score}, file, indent=4)

    def choose_difficulty(self):
        """Choose difficulty level."""

        print("\nChoose Difficulty")
        print("1. Easy (1-20)   Attempts:10")
        print("2. Medium (1-50) Attempts:8")
        print("3. Hard (1-100)  Attempts:6")

        while True:

            choice = input("Enter Choice: ")

            if choice == "1":
                self.secret_number = random.randint(1, 20)
                self.max_attempts = 10
                break

            elif choice == "2":
                self.secret_number = random.randint(1, 50)
                self.max_attempts = 8
                break

            elif choice == "3":
                self.secret_number = random.randint(1, 100)
                self.max_attempts = 6
                break

            else:
                print("Invalid Choice!")

    def play(self):

        self.choose_difficulty()

        attempts_left = self.max_attempts

        while attempts_left > 0:

            try:
                guess = int(input("\nEnter your guess: "))

            except ValueError:
                print("Please enter a valid number.")
                continue

            if guess == self.secret_number:

                self.score = attempts_left * 10

                print("\n🎉 Congratulations!")
                print("You guessed the correct number.")

                print(f"Score : {self.score}")

                high = self.load_high_score()

                if self.score > high:
                    self.save_high_score(self.score)
                    print("🏆 New High Score!")

                return

            elif guess < self.secret_number:
                print("📈 Too Low!")

            else:
                print("📉 Too High!")

            attempts_left -= 1
            print("Attempts Left:", attempts_left)

        print("\nGame Over!")
        print("Secret Number was:", self.secret_number)

    def show_high_score(self):

        print("\n🏆 High Score :", self.load_high_score())


def menu():

    game = NumberGuessingGame()

    while True:

        print("\n" + "=" * 40)
        print("      NUMBER GUESSING GAME")
        print("=" * 40)
        print("1. Play Game")
        print("2. View High Score")
        print("0. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            game.play()

        elif choice == "2":
            game.show_high_score()

        elif choice == "0":
            print("\nThanks for Playing!")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    menu()