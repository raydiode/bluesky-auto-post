import logging
from mySQLauthorisation import MySqlConnector
import os
import sys

class ContentManager:
    def __init__(self):
        self.db_connector = MySqlConnector()

    def check_database(self) -> bool:
        try:
            conn = self.db_connector.getConnection()
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES LIKE 'content'")
            exists = cursor.fetchone() is not None
            cursor.close()
            return exists
        except Exception as e:
            logging.error(f"Database check failed: {e}")
            return False

    def initialize(self):
        if not self.check_database():
            print("Database tables not found. Please set up the database manually.")
            sys.exit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    content_manager = ContentManager()
    content_manager.initialize()

