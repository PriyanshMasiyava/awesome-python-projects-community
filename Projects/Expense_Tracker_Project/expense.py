"""
Expense Model
"""


class Expense:

    def __init__(self, title, category, amount, date, note):

        self.title = title
        self.category = category
        self.amount = amount
        self.date = date
        self.note = note