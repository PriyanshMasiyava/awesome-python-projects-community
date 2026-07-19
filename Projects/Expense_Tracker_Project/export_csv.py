"""
CSV Export Module
"""

import csv
import os
from datetime import datetime


class CSVExporter:

    @staticmethod
    def export(expenses):

        # Folder where this file is located
        project_folder = os.path.dirname(os.path.abspath(__file__))

        # Create exports folder inside project
        export_folder = os.path.join(project_folder, "exports")
        os.makedirs(export_folder, exist_ok=True)

        filename = os.path.join(
            export_folder,
            f"Expense_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Title",
                "Category",
                "Amount",
                "Date",
                "Note"
            ])

            for expense in expenses:
                writer.writerow(expense)

        return filename