"""
Database Operations
"""

import sqlite3

from config import DATABASE_NAME


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE_NAME)

        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                category TEXT NOT NULL,

                amount REAL NOT NULL,

                date TEXT NOT NULL,

                note TEXT

            )
        """) 
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS budget(

                id INTEGER PRIMARY KEY,

                amount REAL

            )
            """)
        self.connection.commit()

    # ---------------- Add ---------------- #

    def add_expense(self, expense):

        self.cursor.execute("""

            INSERT INTO expenses

            (title, category, amount, date, note)

            VALUES (?, ?, ?, ?, ?)

        """, (

            expense.title,

            expense.category,

            expense.amount,

            expense.date,

            expense.note

        ))

        self.connection.commit()

    # ---------------- View ---------------- #

    def get_all_expenses(self):

        self.cursor.execute("""
            SELECT *
            FROM expenses
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()
    # ---------------- Delete ---------------- #

    def delete_expense(self, expense_id):

        self.cursor.execute("""

            DELETE FROM expenses

            WHERE id = ?

        """, (expense_id,))

        self.connection.commit()

    # ---------------- Update ---------------- #

    def update_expense(

        self,

        expense_id,

        title,

        category,

        amount,

        date,

        note

    ):

        self.cursor.execute("""

            UPDATE expenses

            SET

                title=?,

                category=?,

                amount=?,

                date=?,

                note=?

            WHERE id=?

        """, (

            title,

            category,

            amount,

            date,

            note,

            expense_id

        ))

        self.connection.commit()

    # ---------------- Search ---------------- #

    def search_expense(self, keyword):

        self.cursor.execute("""

            SELECT *

            FROM expenses

            WHERE

            title LIKE ?

            OR

            category LIKE ?

        """, (

            "%" + keyword + "%",

            "%" + keyword + "%"

        ))

        return self.cursor.fetchall()
    
    # ---------------- Category Summary ---------------- #

    def get_category_summary(self):

        self.cursor.execute("""

            SELECT

                category,

                SUM(amount)

            FROM expenses

            GROUP BY category

            ORDER BY SUM(amount) DESC

        """)

        return self.cursor.fetchall()
        
    # ---------------- Dashboard ---------------- #

    def get_dashboard_data(self):

        self.cursor.execute("""

            SELECT

                COUNT(*),

                IFNULL(SUM(amount),0),

                IFNULL(MAX(amount),0),

                IFNULL(MIN(amount),0)

            FROM expenses

        """)

        return self.cursor.fetchone()
    
    def set_budget(self, amount):

        self.cursor.execute("DELETE FROM budget")

        self.cursor.execute(

            "INSERT INTO budget VALUES(1, ?)",

            (amount,)

        )

        self.connection.commit()

    def get_budget(self):

        self.cursor.execute(

            "SELECT amount FROM budget WHERE id=1"

        )

        data = self.cursor.fetchone()

        if data:

            return data[0]

        return 0
    
    def get_remaining_budget(self):

        budget = self.get_budget()

        self.cursor.execute(

            "SELECT IFNULL(SUM(amount),0) FROM expenses"

        )

        spent = self.cursor.fetchone()[0]

        return budget - spent
    
    def get_total_expense(self):

        self.cursor.execute(

            "SELECT IFNULL(SUM(amount),0) FROM expenses"

        )

        return self.cursor.fetchone()[0]

        # ---------------- Close ---------------- #

    def close(self):

        self.connection.close()