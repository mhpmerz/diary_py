"""This module helps in creating and maintaining the database"""

import sqlite3

class Database:
    """The main class for using the database throughout the project"""
    def __init__(self, db_path="datenbank.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access by column name
        self.cur = self.conn.cursor()

    def query(self, sql, params=()):
        """query the database"""
        self.cur.execute(sql, params)
        return self.cur.fetchall()

    def execute(self, sql, params=()):
        """execute a statement on the database"""
        self.cur.execute(sql, params)
        self.conn.commit()

    def close(self):
        """close the database"""
        self.conn.close()

# Global instance on startup
db = Database()
