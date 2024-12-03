import mysql.connector
from typing import Optional
import logging
from dotenv import load_dotenv
import os

class MySqlConnector:
   def __init__(self):
       load_dotenv()
       self._conn = None
       self._connect()

   def _connect(self) -> None:
       """Establish database connection using environment variables"""
       try:
           self._conn = mysql.connector.connect(
               host=os.getenv('DB_HOST'),
               user=os.getenv('DB_USER'),
               password=os.getenv('DB_PASSWORD'),
               database=os.getenv('DB_NAME')
           )
       except mysql.connector.Error as err:
           logging.error(f"Database connection failed: {err}")
           raise

   def disconnect(self) -> None:
       """Safely close database connection"""
       if self._conn and self._conn.is_connected():
           self._conn.close()

   def getConnection(self):
       """Return active connection or reconnect if needed"""
       if not self._conn or not self._conn.is_connected():
           self._connect()
       return self._conn

   def __enter__(self):
       return self

   def __exit__(self, exc_type, exc_val, exc_tb):
       self.disconnect()
