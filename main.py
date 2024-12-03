from contentManager import ContentManager
from databaseChecker import ContentManager as DBManager
from appSettings import TEST_MODE, POST_INTERVAL_MINUTES, TEST_INTERVAL
from addContent import ContentAdder
import time
import logging
import sys

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize database
    db_manager = DBManager()
    db_manager.initialize()

    # Add content from markdown files
    adder = ContentAdder()
    adder.process_markdown_files('content')

    # Initialize content manager
    content_manager = ContentManager()

    logger.info("Bluesky Bot Starting...")
    logger.info(f"Running in {'TEST' if TEST_MODE else 'PRODUCTION'} mode")

    try:
        while True:
            # Attempt to post content
            success = content_manager.post_content()
            
            if success:
                logger.info("Post successful")
            else:
                logger.info("No content to post or posting failed")

            # Sleep based on mode
            interval = TEST_INTERVAL if TEST_MODE else POST_INTERVAL_MINUTES * 60
            logger.info(f"Waiting {interval} seconds until next post attempt")
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Bot shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
