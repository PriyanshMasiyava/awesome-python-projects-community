import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from export_csv import CSVExporter
import os

from pdf_report import PDFExporter
from analytics import ExpenseAnalytics
from config import APP_TITLE
from config import WINDOW_WIDTH
from config import WINDOW_HEIGHT
from theme import *
from database import Database
from expense import Expense
from tkcalendar import DateEntry


class ExpenseTrackerApp:

    def __init__(self):

        self.database = Database()

        self.root = tk.Tk()

        self.root.title(APP_TITLE)

        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.theme = LIGHT_THEME

        self.root.configure(bg=self.theme["bg"])

        self.create_header()
        self.show_database_status()
        self.create_dashboard()   # <-- Add this
        self.create_toolbar()
        self.create_search()
        self.create_table()
        self.load_expenses()
    def create_header(self):

        title = tk.Label(

            self.root,

            text="Expense Tracker Pro",

            font=("Segoe UI", 24, "bold"),

            bg=self.theme["bg"],

            fg=self.theme["fg"]

        )

        title.pack(pady=20)

        subtitle = tk.Label(

            self.root,

            text="Manage your daily expenses professionally.",

            font=("Segoe UI", 12),

            bg=self.theme["bg"],

            fg="gray"

        )

        subtitle.pack()

    def show_database_status(self):

        status = tk.Label(

            self.root,

            text="✅ Database Connected Successfully",

            font=("Segoe UI", 11),

            bg=self.theme["bg"],

            fg="green"

        )

        status.pack(pady=10)

    def create_dashboard(self):

        dashboard = tk.Frame(
            self.root,
            bg=self.theme["bg"]
        )

        dashboard.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.total_expense = tk.Label(
            dashboard,
            text="₹0",
            font=("Segoe UI",14,"bold"),
            fg="green",
            bg=self.theme["bg"]
        )

        self.total_expense.grid(row=0,column=0,padx=25)

        self.total_records = tk.Label(
            dashboard,
            text="0 Records",
            font=("Segoe UI",14,"bold"),
            bg=self.theme["bg"]
        )

        self.total_records.grid(row=0,column=1,padx=25)

        self.highest = tk.Label(
            dashboard,
            text="Highest ₹0",
            font=("Segoe UI",14,"bold"),
            bg=self.theme["bg"]
        )

        self.highest.grid(row=0,column=2,padx=25)

        self.lowest = tk.Label(
            dashboard,
            text="Lowest ₹0",
            font=("Segoe UI",14,"bold"),
            bg=self.theme["bg"]
        )

        self.lowest.grid(row=0,column=3,padx=25)

        self.budget = tk.Label(
        dashboard,
        text="Budget ₹0",
        font=("Segoe UI",14,"bold"),
        bg=self.theme["bg"]
        )

        self.budget.grid(row=0,column=4,padx=20)

        self.remaining = tk.Label(
            dashboard,
            text="Remaining ₹0",
            font=("Segoe UI",14,"bold"),
            fg="blue",
            bg=self.theme["bg"]
        )

        self.remaining.grid(row=0,column=5,padx=20)

        # ---------------- Budget Progress ---------------- #

        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=500,
            mode="determinate"
        )

        self.progress.pack(pady=10)

        self.progress_label = tk.Label(
            self.root,
            text="Budget Usage : 0%",
            font=("Segoe UI",11,"bold"),
            bg=self.theme["bg"]
        )

        self.progress_label.pack()

        self.refresh_dashboard()

    def create_toolbar(self):

        toolbar = tk.Frame(
            self.root,
            bg=self.theme["bg"]
        )

        toolbar.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Add Expense Button
        tk.Button(
            toolbar,
            text="➕ Add Expense",
            width=15,
            command=self.open_add_expense_window
        ).pack(side="left", padx=5)

        # Update Button
        tk.Button(
            toolbar,
            text="✏ Update",
            width=15,
            command=self.open_update_window
            ).pack(side="left", padx=5)

        # Delete Button
        tk.Button(
            toolbar,
            text="🗑 Delete",
            width=15,
            command=self.delete_expense
            ).pack(side="left", padx=5)

        # CSV Button
        tk.Button(
            toolbar,
            text="📤 CSV",
            width=12,
            command=self.export_csv
            ).pack(side="left", padx=5)

        # PDF Button
        tk.Button(
            toolbar,
            text="📄 PDF",
            width=12,
            command=self.export_pdf
        ).pack(side="left", padx=5)

        # Budget Button
        tk.Button(
            toolbar,
            text="💳 Budget",
            width=12,
            command=self.open_budget_window
        ).pack(side="left", padx=5)

        # Analytics Button
        tk.Button(
            toolbar,
            text="📊 Analytics",
            width=12,
            command=self.show_analytics
        ).pack(side="left", padx=5)
    def create_search(self):

        frame = tk.Frame(
        self.root,
        bg=self.theme["bg"]
        )

        frame.pack(
        fill="x",
        padx=20,
        pady=10
        )

        tk.Label(
        frame,
        text="Search:",
        bg=self.theme["bg"]
        ).pack(side="left")

        self.search_entry = tk.Entry(
        frame,
        width=40
        )

        self.search_entry.pack(
        side="left",
        padx=10
        )

        tk.Button(
            frame,
            text="🔍 Search",
            command=self.search_expense
            ).pack(side="left", padx=5)

        tk.Button(
            frame,
            text="🔄 Refresh",
            command=self.refresh_all
            ).pack(side="left", padx=5)
        

    def create_table(self):

        columns = (
        "ID",
        "Title",
        "Category",
        "Amount",
        "Date",
        "Note"
        )

        self.table = ttk.Treeview(
        self.root,
        columns=columns,
        show="headings",
        height=18
        )

        for column in columns:
            self.table.heading(column, text=column)
            if column == "ID":
                    width = 60
            elif column == "Title":
                    width = 180
            elif column == "Category":
                    width = 120
            elif column == "Amount":
                    width = 100
            elif column == "Date":
                    width = 120
            else:
                    width = 250

            self.table.column(column, width=width, anchor="center")

        self.table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
        )   
    
    def load_expenses(self):

        # Remove old rows
        for row in self.table.get_children():
            self.table.delete(row)

        # Fetch all expenses
        expenses = self.database.get_all_expenses()

        # Insert into Treeview
        for expense in expenses:
            self.table.insert("", "end", values=expense)
    
    def save_expense(self):

        title = self.title_entry.get().strip()

        category = self.category_combo.get()

        amount = self.amount_entry.get().strip()

        date = self.date_entry.get()

        note = self.note_entry.get().strip()

        if title == "" or amount == "":
            messagebox.showerror(
                "Error",
                "Please fill all required fields."
            )
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be a number."
            )
            return

        expense = Expense(
            title,
            category,
            amount,
            date,
            note
        )

        self.database.add_expense(expense)

        messagebox.showinfo(
            "Success",
            "Expense added successfully."
        )

        self.load_expenses()

        self.refresh_dashboard()

        self.add_window.destroy()
    def open_add_expense_window(self):

        self.add_window = tk.Toplevel(self.root)

        self.add_window.title("Add Expense")

        self.add_window.geometry("450x500")

        self.add_window.resizable(False, False)

        tk.Label(
            self.add_window,
            text="Add New Expense",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        # ---------------- Title ----------------

        tk.Label(
            self.add_window,
            text="Expense Title"
        ).pack(anchor="w", padx=20)

        self.title_entry = tk.Entry(
            self.add_window,
            width=40
        )

        self.title_entry.pack(pady=5)

        # ---------------- Category ----------------

        tk.Label(
            self.add_window,
            text="Category"
        ).pack(anchor="w", padx=20)

        self.category_combo = ttk.Combobox(
            self.add_window,
            width=37,
            state="readonly"
        )

        self.category_combo["values"] = (
            "Food",
            "Travel",
            "Shopping",
            "Medical",
            "Education",
            "Entertainment",
            "Bills",
            "Rent",
            "Others"
        )

        self.category_combo.current(0)

        self.category_combo.pack(pady=5)

        # ---------------- Amount ----------------

        tk.Label(
            self.add_window,
            text="Amount"
        ).pack(anchor="w", padx=20)

        self.amount_entry = tk.Entry(
            self.add_window,
            width=40
        )

        self.amount_entry.pack(pady=5)

        # ---------------- Date ----------------

        tk.Label(
            self.add_window,
            text="Date"
        ).pack(anchor="w", padx=20)

        self.date_entry = DateEntry(
            self.add_window,
            width=37,
            date_pattern="dd-mm-yyyy"
        )

        self.date_entry.pack(pady=5)

        # ---------------- Note ----------------

        tk.Label(
            self.add_window,
            text="Note"
        ).pack(anchor="w", padx=20)

        self.note_entry = tk.Entry(
            self.add_window,
            width=40
        )

        self.note_entry.pack(pady=5)

        # ---------------- Save Button ----------------

        tk.Button(
            self.add_window,
            text="💾 Save Expense",
            bg="green",
            fg="white",
            width=20,
            command=self.save_expense
        ).pack(pady=25)
    
    def update_expense(self):

        title = self.update_title.get().strip()

        category = self.update_category.get()

        amount = self.update_amount.get().strip()

        date = self.update_date.get()

        note = self.update_note.get().strip()

        if title == "" or amount == "":
            messagebox.showerror(
                "Error",
                "Please fill all required fields."
            )
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be numeric."
            )
            return

        self.database.update_expense(
            self.expense_id,
            title,
            category,
            amount,
            date,
            note
        )

        messagebox.showinfo(
            "Success",
            "Expense Updated Successfully."
        )

        self.update_window.destroy()

        self.load_expenses()
        self.refresh_dashboard()
    def open_update_window(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select an expense."
            )
            return

        item = self.table.item(selected)

        values = item["values"]

        self.expense_id = values[0]

        self.update_window = tk.Toplevel(self.root)

        self.update_window.title("Update Expense")

        self.update_window.geometry("450x500")

        self.update_window.resizable(False, False)

        tk.Label(
            self.update_window,
            text="Update Expense",
            font=("Segoe UI",18,"bold")
        ).pack(pady=15)

        # Title
        tk.Label(self.update_window,text="Title").pack(anchor="w",padx=20)

        self.update_title = tk.Entry(
            self.update_window,
            width=40
        )

        self.update_title.pack(pady=5)

        self.update_title.insert(0, values[1])

        # Category
        tk.Label(self.update_window,text="Category").pack(anchor="w",padx=20)

        self.update_category = ttk.Combobox(
            self.update_window,
            width=37,
            state="readonly",
            values=[
                "Food",
                "Travel",
                "Shopping",
                "Medical",
                "Education",
                "Entertainment",
                "Bills",
                "Rent",
                "Others"
            ]
        )

        self.update_category.pack(pady=5)

        self.update_category.set(values[2])

        # Amount
        tk.Label(self.update_window,text="Amount").pack(anchor="w",padx=20)

        self.update_amount = tk.Entry(
            self.update_window,
            width=40
        )

        self.update_amount.pack(pady=5)

        self.update_amount.insert(0, values[3])

        # Date
        tk.Label(self.update_window,text="Date").pack(anchor="w",padx=20)

        self.update_date = DateEntry(
            self.update_window,
            width=37,
            date_pattern="dd-mm-yyyy"
        )

        self.update_date.pack(pady=5)

        self.update_date.set_date(values[4])

        # Note
        tk.Label(self.update_window,text="Note").pack(anchor="w",padx=20)

        self.update_note = tk.Entry(
            self.update_window,
            width=40
        )

        self.update_note.pack(pady=5)

        self.update_note.insert(0, values[5])

        tk.Button(
            self.update_window,
            text="💾 Update Expense",
            bg="green",
            fg="white",
            width=20,
            command=self.update_expense
        ).pack(pady=20)
    
    def search_expense(self):

        keyword = self.search_entry.get().strip()

        if keyword == "":
            self.load_expenses()
            return

        expenses = self.database.search_expense(keyword)

        # Clear current rows
        for row in self.table.get_children():
            self.table.delete(row)

        # Show search results
        for expense in expenses:
            self.table.insert("", tk.END, values=expense)

        if not expenses:
            messagebox.showinfo(
                "Search",
                "No matching expenses found."
            )

# Add here
    def refresh_all(self):

        self.search_entry.delete(0, tk.END)

        self.load_expenses()

        self.refresh_dashboard()


# Existing method
    def delete_expense(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select an expense."
            )
            return

        item = self.table.item(selected)

        expense_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Delete",
            "Are you sure you want to delete this expense?"
        )

        if confirm:

            self.database.delete_expense(expense_id)

            self.load_expenses()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Success",
                "Expense deleted successfully."
            )
    
    def export_csv(self):

        expenses = self.database.get_all_expenses()

        if not expenses:
            messagebox.showwarning(
                "Export",
                "No expenses available."
            )
            return

        filename = CSVExporter.export(expenses)

        messagebox.showinfo(
            "Success",
            "CSV Exported Successfully."
        )

        os.startfile(filename)
        # Generate PDF once
        self.export_pdf()

    def export_pdf(self):

        expenses = self.database.get_all_expenses()

        if not expenses:
            messagebox.showwarning(
                "Export",
                "No expenses available."
            )
            return

        try:
            filename = PDFExporter.export(expenses)

            print("PDF Saved At:", filename)

            messagebox.showinfo(
                "Success",
                f"PDF Generated Successfully.\n{filename}"
            )

            os.startfile(os.path.abspath(filename))

        except Exception as e:
            messagebox.showerror(
                "PDF Error",
                str(e)
            )
            

    def refresh_dashboard(self):

        data = self.database.get_dashboard_data()

        total_records = data[0]
        total_amount = data[1]
        highest = data[2]
        lowest = data[3]

        budget = self.database.get_budget()
        remaining = self.database.get_remaining_budget()
        spent = self.database.get_total_expense()

        # ---------------- Dashboard Cards ---------------- #

        self.total_expense.config(
            text=f"💰 ₹{total_amount:.2f}"
        )

        self.total_records.config(
            text=f"📋 {total_records} Records"
        )

        self.highest.config(
            text=f"📈 ₹{highest:.2f}"
        )

        self.lowest.config(
            text=f"📉 ₹{lowest:.2f}"
        )

        self.budget.config(
            text=f"💳 ₹{budget:.2f}"
        )

        # Remaining Budget Color
        if remaining >= 0:

            self.remaining.config(
                text=f"💵 ₹{remaining:.2f}",
                fg="green"
            )

        else:

            self.remaining.config(
                text=f"💵 ₹{remaining:.2f}",
                fg="red"
            )

        # ---------------- Budget Progress ---------------- #

        if budget > 0:

            percent = (spent / budget) * 100

            # Progressbar maximum is 100
            self.progress["value"] = min(percent, 100)

            if percent >= 100:

                self.progress_label.config(
                    text="❌ Budget Exceeded!",
                    fg="red"
                )

            elif percent >= 80:

                self.progress_label.config(
                    text=f"⚠ Budget Usage : {percent:.1f}%",
                    fg="orange"
                )

            else:

                self.progress_label.config(
                    text=f"✅ Budget Usage : {percent:.1f}%",
                    fg="green"
                )

        else:

            self.progress["value"] = 0

            self.progress_label.config(
                text="Budget Not Set",
                fg="blue"
            )

    def on_closing(self):

        self.database.close()

        self.root.destroy()

    def open_budget_window(self):

        self.budget_window = tk.Toplevel(self.root)

        self.budget_window.title("Monthly Budget")

        self.budget_window.geometry("350x180")

        self.budget_window.resizable(False, False)

        tk.Label(
            self.budget_window,
            text="Set Monthly Budget",
            font=("Segoe UI",16,"bold")
        ).pack(pady=15)

        self.budget_entry = tk.Entry(
            self.budget_window,
            width=25,
            font=("Segoe UI",12)
        )

        self.budget_entry.pack(pady=10)

        tk.Button(
            self.budget_window,
            text="💾 Save Budget",
            bg="green",
            fg="white",
            width=18,
            command=self.save_budget
        ).pack(pady=10)
    
    def save_budget(self):

        amount = self.budget_entry.get().strip()

        if amount == "":
            messagebox.showerror(
                "Error",
                "Enter Budget Amount."
            )
            return

        try:
            amount = float(amount)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Budget must be numeric."
            )
            return

        self.database.set_budget(amount)

        messagebox.showinfo(
            "Success",
            "Budget Saved Successfully."
        )

        self.budget_window.destroy()

        self.refresh_dashboard()
    def show_analytics(self):

        print("Analytics button clicked")

        try:
            ExpenseAnalytics(
                self.root,
                self.database
            )

            print("Analytics window opened")

        except Exception as e:
            print("ERROR:", e)
            messagebox.showerror(
                "Analytics Error",
                str(e)
            )

    def run(self):

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_closing
        )

        self.root.mainloop()