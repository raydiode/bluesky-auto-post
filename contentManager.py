from blueskyAuth import BlueskyAuth
from mySQLauthorisation import MySqlConnector
from datetime import datetime
from appSettings import TEST_MODE
import time
import logging

class ContentManager:
   def __init__(self):
       self.bluesky_auth = BlueskyAuth()
       self.db_connector = MySqlConnector()
       # Login once at initialization
       if not self.bluesky_auth.login():
           logging.error("Initial Bluesky login failed")

   def get_next_post(self):
       """Get next pending post from database"""
       conn = self.db_connector.getConnection()
       cursor = conn.cursor(dictionary=True)

       try:
           query = """
               SELECT * FROM content
               WHERE status = 'pending'
               ORDER BY post_number ASC
               LIMIT 1
           """
           cursor.execute(query)
           return cursor.fetchone()
       finally:
           cursor.close()

   def update_post_status(self, post_id: int, status: str, bluesky_id: str = None):
       """Update post status and related fields in database"""
       conn = self.db_connector.getConnection()
       cursor = conn.cursor()

       try:
           query = """
               UPDATE content
               SET status = %s,
                   post_datetime = %s,
                   bluesky_post_id = %s
               WHERE id = %s
           """
           cursor.execute(query, (status, datetime.now(), bluesky_id, post_id))
           conn.commit()
       except Exception as e:
           logging.error(f"Failed to update post status: {e}")
           conn.rollback()
           raise
       finally:
           cursor.close()

   def post_content(self):
       """Main method to post content to Bluesky"""
       if not self.bluesky_auth.isAuthenticated():
           if not self.bluesky_auth.login():
               logging.error("Failed to login to Bluesky")
               return False

       # Get the next post
       post = self.get_next_post()
       if not post:
           logging.info("No pending posts found")
           return False

       if TEST_MODE:
           logging.info(f"TEST MODE: Would post content: {post['content']}")
           return True

       client = self.bluesky_auth.getClient()

       try:
           # Attempt to post to Bluesky
           response = client.post(text=post['content'])

           # Update database with success
           self.update_post_status(
               post_id=post['id'],
               status='posted',
               bluesky_id=response['uri']
           )
           logging.info(f"Successfully posted content ID {post['id']}")
           return True

       except Exception as e:
           # Update database with failure
           self.update_post_status(
               post_id=post['id'],
               status='failed'
           )
           logging.error(f"Failed to post content ID {post['id']}: {e}")
           return False

if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO)
   manager = ContentManager()
   manager.post_content()
