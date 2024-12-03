from mySQLauthorisation import MySqlConnector
import logging
import sys
import os
import glob

class ContentAdder:
    def __init__(self):
        self.db_connector = MySqlConnector()

    def read_markdown_file(self, filepath: str) -> tuple[str, str]:
        """Read content and theme from markdown file"""
        try:
            with open(filepath, 'r') as file:
                content = file.read().strip()
                # Use filename without extension as theme
                theme = os.path.splitext(os.path.basename(filepath))[0]
                return content, theme
        except Exception as e:
            logging.error(f"Failed to read markdown file {filepath}: {e}")
            return None, None

    def insert_content(self, content: str, theme: str = None) -> bool:
        """Insert new content into database"""
        conn = self.db_connector.getConnection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT MAX(post_number) FROM content")
            max_post = cursor.fetchone()[0]
            next_post = 1 if max_post is None else max_post + 1

            query = """
                INSERT INTO content 
                (content, theme, status, post_number) 
                VALUES (%s, %s, 'pending', %s)
            """
            cursor.execute(query, (content, theme, next_post))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to insert content: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def process_markdown_files(self, directory: str = 'content'):
        """Process all markdown files in the specified directory"""
        if not os.path.exists(directory):
            print(f"Directory '{directory}' not found.")
            return

        markdown_files = glob.glob(os.path.join(directory, '*.md'))
        
        if not markdown_files:
            print(f"No markdown files found in '{directory}'")
            return

        for filepath in markdown_files:
            content, theme = self.read_markdown_file(filepath)
            if content:
                if self.insert_content(content, theme):
                    print(f"Successfully added content from {filepath}")
                else:
                    print(f"Failed to add content from {filepath}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Get directory from command line argument or use default
    directory = sys.argv[1] if len(sys.argv) > 1 else 'content'
    
    adder = ContentAdder()
    adder.process_markdown_files(directory)
