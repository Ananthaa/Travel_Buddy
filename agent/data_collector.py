import json
import sqlite3
import os
from datetime import datetime

class DataCollectionAgent:
    def __init__(self, db_path="travel_buddy_v3.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT NOT NULL,
                destination TEXT,
                start_location TEXT,
                travel_mode TEXT,
                travel_date TEXT,
                duration INTEGER,
                travelers_count INTEGER,
                budget TEXT,
                travel_style TEXT,
                food_habits TEXT,
                interests TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def save_preferences(self, data):
        """
        Saves user preferences to the database.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO preferences (
                    name, email, destination, start_location, travel_mode, 
                    travel_date, duration, travelers_count, budget, 
                    travel_style, food_habits, interests
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('name'),
                data.get('email'),
                data.get('destination'),
                data.get('start_location'),
                data.get('travel_mode'),
                data.get('travel_date'),
                data.get('duration'),
                data.get('travelers_count'),
                data.get('budget'),
                data.get('travel_style'),
                data.get('food_habits'),
                data.get('interests')
            ))
            conn.commit()
            conn.close()
            return True, "Preferences saved successfully."
        except Exception as e:
            return False, str(e)

    def get_all_preferences(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM preferences')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
