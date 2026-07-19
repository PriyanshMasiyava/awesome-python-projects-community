"""
Expense Analytics Module
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


class ExpenseAnalytics:

    def __init__(self, parent, database):

        self.database = database

        self.window = tk.Toplevel(parent)
        self.window.title("Expense Analytics")
        self.window.geometry("900x650")
        self.window.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        summary = self.database.get_category_summary()

        title = tk.Label(
            self.window,
            text="Expense Analytics Dashboard",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=15)

        if not summary:

            tk.Label(
                self.window,
                text="No Expense Data Found",
                font=("Segoe UI", 15)
            ).pack(pady=100)

            return

        total_amount = sum(row[1] for row in summary)
        total_categories = len(summary)
        average = total_amount / total_categories

        highest = summary[0]
        lowest = summary[-1]

        # ---------------- Statistics ---------------- #

        stats = tk.Frame(self.window)
        stats.pack(fill="x", padx=20)

        tk.Label(
            stats,
            text=f"💰 Total Expense\n₹ {total_amount:.2f}",
            font=("Segoe UI", 12, "bold"),
            relief="groove",
            width=20,
            pady=10
        ).grid(row=0, column=0, padx=10)

        tk.Label(
            stats,
            text=f"📂 Categories\n{total_categories}",
            font=("Segoe UI", 12, "bold"),
            relief="groove",
            width=20,
            pady=10
        ).grid(row=0, column=1, padx=10)

        tk.Label(
            stats,
            text=f"📈 Average\n₹ {average:.2f}",
            font=("Segoe UI", 12, "bold"),
            relief="groove",
            width=20,
            pady=10
        ).grid(row=0, column=2, padx=10)

        # ---------------- Highest & Lowest ---------------- #

        frame = tk.Frame(self.window)
        frame.pack(fill="x", padx=20, pady=15)

        highest_card = tk.LabelFrame(
            frame,
            text="Highest Spending",
            padx=20,
            pady=15
        )

        highest_card.pack(side="left", expand=True, fill="x", padx=10)

        tk.Label(
            highest_card,
            text=highest[0],
            font=("Segoe UI", 16, "bold")
        ).pack()

        tk.Label(
            highest_card,
            text=f"₹ {highest[1]:.2f}",
            font=("Segoe UI", 14),
            fg="green"
        ).pack()

        lowest_card = tk.LabelFrame(
            frame,
            text="Lowest Spending",
            padx=20,
            pady=15
        )

        lowest_card.pack(side="left", expand=True, fill="x", padx=10)

        tk.Label(
            lowest_card,
            text=lowest[0],
            font=("Segoe UI", 16, "bold")
        ).pack()

        tk.Label(
            lowest_card,
            text=f"₹ {lowest[1]:.2f}",
            font=("Segoe UI", 14),
            fg="red"
        ).pack()

        # ---------------- Table ---------------- #

        columns = ("Category", "Amount")

        table = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            height=10
        )

        table.heading("Category", text="Category")
        table.heading("Amount", text="Total Expense")

        table.column("Category", width=300, anchor="center")
        table.column("Amount", width=200, anchor="center")

        for row in summary:

            table.insert(
                "",
                tk.END,
                values=(
                    row[0],
                    f"₹ {row[1]:.2f}"
                )
            )

        table.pack(fill="both", expand=True, padx=20, pady=15)

        # ---------------- Buttons ---------------- #

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="📊 Bar Chart",
            width=20,
            command=self.show_bar_chart
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="🥧 Pie Chart",
            width=20,
            command=self.show_pie_chart
        ).pack(side="left", padx=10)

    # ---------------- Bar Chart ---------------- #

    def show_bar_chart(self):

        summary = self.database.get_category_summary()

        if not summary:
            return

        categories = [row[0] for row in summary]
        amounts = [row[1] for row in summary]

        plt.figure(figsize=(9,5))
        plt.bar(categories, amounts)
        plt.title("Expense by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.show()

    # ---------------- Pie Chart ---------------- #

    def show_pie_chart(self):

        summary = self.database.get_category_summary()

        if not summary:
            return

        categories = [row[0] for row in summary]
        amounts = [row[1] for row in summary]

        plt.figure(figsize=(7,7))

        plt.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Expense Distribution")
        plt.tight_layout()
        plt.show()