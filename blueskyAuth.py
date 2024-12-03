from atproto import Client
import os
import logging
from dotenv import load_dotenv

class BlueskyAuth:
   def __init__(self):
       load_dotenv()
       self._client = Client()
       self._isLoggedIn = False

   def login(self) -> bool:
       """Authenticate with Bluesky using credentials from .env"""
       try:
           username = os.getenv('BLUESKY_USERNAME')
           password = os.getenv('BLUESKY_PASSWORD')

           if not username or not password:
               logging.error("Missing Bluesky credentials in environment variables")
               return False

           self._client.login(username, password)
           self._isLoggedIn = True
           logging.info("Successfully logged in to Bluesky")
           return True

       except Exception as e:
           logging.error(f"Bluesky login error: {str(e)}")
           return False

   def getClient(self):
       """Return authenticated client if logged in"""
       if not self._isLoggedIn:
           self.login()
       return self._client

   def isAuthenticated(self) -> bool:
       """Check if currently authenticated"""
       return self._isLoggedIn
