from typing import Final

# Application Mode
TEST_MODE: Final[bool] = True

# Posting Schedule
POST_INTERVAL_MINUTES: Final[int] = 600  # 10 hours between posts
MAX_DAILY_POSTS: Final[int] = 2

# Error Handling
RETRY_DELAY_SECONDS: Final[int] = 60

# Test Mode Settings
TEST_INTERVAL: Final[int] = 10  # Seconds between posts in test mode

# Validation
def validate_settings() -> bool:
    """Validate that settings are within acceptable ranges."""
    if POST_INTERVAL_MINUTES <= 0:
        raise ValueError("POST_INTERVAL_MINUTES must be positive")
    if MAX_DAILY_POSTS <= 0:
        raise ValueError("MAX_DAILY_POSTS must be positive")
    if RETRY_DELAY_SECONDS <= 0:
        raise ValueError("RETRY_DELAY_SECONDS must be positive")
    if TEST_INTERVAL <= 0:
        raise ValueError("TEST_INTERVAL must be positive")
    return True
