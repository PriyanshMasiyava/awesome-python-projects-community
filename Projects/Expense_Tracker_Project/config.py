"""
===========================================
Expense Tracker Configuration File
===========================================
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_FOLDER = os.path.join(BASE_DIR, "database")

DATABASE_NAME = os.path.join(DATABASE_FOLDER, "expense_tracker.db")

APP_TITLE = "Expense Tracker Pro"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

DEFAULT_THEME = "light"

CURRENCY = "₹"

EXPORT_FOLDER = "exports"