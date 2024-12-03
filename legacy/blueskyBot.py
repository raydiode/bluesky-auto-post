from atproto import Client
import os
import time
import logging
from datetime import datetime
from contentFetcher import ContentFetcher
from botSettings import POST_INTERVAL_MINUTES, MAX_DAILY_POSTS, RETRY_DELAY_SECONDS, TEST_MODE
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv()

# Configure logging to track bot's operation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot.log'
)

class Database:
    def __init__(self):
        # Initialize database connection using environment variables
        self.conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content TEXT,
                posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_content (content(255))
            )
        ''')
        self.conn.commit()

    def content_exists(self, content):
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM posts WHERE content = %s', (content,))
        return cursor.fetchone() is not None

    def add_content(self, content):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO posts (content) VALUES (%s)', (content,))
        self.conn.commit()

class BlueskyBot:
    def __init__(self):
        # Initialize bot components
        self.client = Client()
        self.is_logged_in = False
        self.contentFetcher = ContentFetcher()
        self.posts_today = 0
        self.last_post_date = None
        self.db = Database()

    def login(self):
        try:
            username = os.getenv('BLUESKY_USERNAME')
            password = os.getenv('BLUESKY_PASSWORD')
            
            if not username or not password:
                logging.error("Missing credentials in environment variables")
                return False
                
            self.client.login(username, password)
            self.is_logged_in = True
            logging.info("Successfully logged in")
            return True
            
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            return False

    def should_post(self):
        # Reset daily post count if it's a new day
        current_time = datetime.now()
        if self.last_post_date and current_time.date() != self.last_post_date.date():
            self.posts_today = 0
            
        # Check if we've reached daily post limit
        if self.posts_today >= MAX_DAILY_POSTS:
            logging.info("Daily post limit reached")
            return False
            
        return True

    def post_content(self):
        if not self.is_logged_in:
            logging.error("Not logged in")
            return False

        content = self.contentFetcher.get_content()
        if content is None:
            logging.info("No content available")
            return False

        if self.db.content_exists(content):
            logging.info("Content already posted")
            return False

        # Handle test mode differently than production mode
        if TEST_MODE:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"\nTest Post at {current_time}:")
            print(content)
            return True

        try:
            self.client.post(text=content)
            self.posts_today += 1
            self.last_post_date = datetime.now()
            self.db.add_content(content)
            logging.info("Posted successfully")
            return True
            
        except Exception as e:
            logging.error(f"Post error: {str(e)}")
            return False

    def run(self):
        # Main bot execution loop
        if not self.login():
            return
            
        while True:
            try:
                if self.should_post():
                    if TEST_MODE:
                        # In test mode, fetch and display content every 15 seconds
                        content = self.contentFetcher.get_content()
                        if content:
                            current_time = datetime.now().strftime("%H:%M:%S")
                            print(f"\nTest Post at {current_time}:")
                            print(content)
                        time.sleep(15)  # Test mode interval
                    else:
                        # In production mode, post content and wait for normal interval
                        self.post_content()
                        time.sleep(POST_INTERVAL_MINUTES * 60)
                        
            except Exception as e:
                logging.error(f"Runtime error: {str(e)}")
                time.sleep(RETRY_DELAY_SECONDS)

# Entry point for the script
if __name__ == "__main__":
    bot = BlueskyBot()
    bot.run()
