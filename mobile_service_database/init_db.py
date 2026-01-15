#!/usr/bin/env python3
"""Initialize SQLite database for the Mobile Service Website.

Creates/updates the minimal schema needed by the Flask backend:
- services: list of service offerings for the Services section
- customer_requests: stores customer form submissions

This script is safe to run multiple times.
"""

import os
import sqlite3

DB_NAME = "myapp.db"

print("Starting SQLite setup for Mobile Service Website...")

db_exists = os.path.exists(DB_NAME)
if db_exists:
    print(f"SQLite database already exists at {DB_NAME}")
else:
    print("Creating new SQLite database...")

conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Enable foreign keys (good practice even if not used heavily).
cursor.execute("PRAGMA foreign_keys = ON")

# Core schema
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        icon TEXT,
        price_hint TEXT,
        sort_order INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS customer_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        mobile_model TEXT NOT NULL,
        problem TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
)

# Lightweight content tables for About/Contact (optional but convenient)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS site_content (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
)

# Seed services if empty
cursor.execute("SELECT COUNT(*) AS c FROM services")
count = cursor.fetchone()["c"]
if count == 0:
    cursor.executemany(
        """
        INSERT INTO services (title, description, icon, price_hint, sort_order)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                "Screen Replacement",
                "Cracked, unresponsive, or flickering displays. Fast assessment and quality parts.",
                "📱",
                "Typical: $79–$249",
                1,
            ),
            (
                "Battery & Charging",
                "Battery draining quickly or device not charging. Diagnostics and replacements.",
                "🔋",
                "Typical: $49–$129",
                2,
            ),
            (
                "Software Troubleshooting",
                "Slow performance, boot loops, app crashes, updates, and data migration support.",
                "🧠",
                "Typical: $39–$99",
                3,
            ),
            (
                "Water Damage Check",
                "Inspection, cleaning guidance, and next-step recommendations.",
                "💧",
                "Assessment: $29+",
                4,
            ),
        ],
    )
    print("Seeded default services.")

# Seed site content if missing
defaults = {
    "about_description": "We provide practical, honest mobile repair and troubleshooting. Our goal is to get your device working with clear options and fair pricing.",
    "contact_hours": "Mon–Sat: 9am–7pm • Sun: 11am–4pm",
    "contact_phone": "+1 (555) 123-4567",
    "contact_email": "support@example.com",
}
for k, v in defaults.items():
    cursor.execute("INSERT OR IGNORE INTO site_content (key, value) VALUES (?, ?)", (k, v))

conn.commit()
conn.close()

print("SQLite setup complete.")
print(f"Database: {DB_NAME}")
print(f"Location: {os.path.abspath(DB_NAME)}")
print("Script completed successfully.")
