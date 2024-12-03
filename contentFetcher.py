import mysql.connector
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ContentFetcher:
    def __init__(self):
        # Establish database connection using environment variables
        self.conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

    def get_content(self):
        cursor = self.conn.cursor()
        try:
            # Query the posts table in bluesky_content database
            # Returns a random piece of content using ORDER BY RAND()
            cursor.execute('''
                SELECT content FROM bluesky_content.posts
                ORDER BY RAND()
                LIMIT 1
            ''')
            content = cursor.fetchone()
            return content[0] if content else None
        except Exception as e:
            # Log any errors that occur during content fetching
            logging.error(f"Error fetching content: {str(e)}")
            return None

    def __del__(self):
        # Ensure database connection is closed when object is destroyed
        self.conn.close()
