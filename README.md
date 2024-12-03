# Bluesky Content Bot

Automated content posting bot for Bluesky social network.

## Features
- Scheduled content posting
- Markdown file processing
- MySQL database integration 
- Test & Production modes

## Prerequisites
- Python 3.8+
- MySQL database
- Bluesky account

## Installation
```bash
git clone [repository]
pip install -r requirements.txt
```

## Configuration

### Environment Variables
```
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
BLUESKY_USERNAME=
BLUESKY_PASSWORD=
```

### Database Setup
```sql
CREATE TABLE content (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    theme VARCHAR(255),
    status ENUM('pending', 'posted', 'failed'),
    post_number INT,
    post_datetime DATETIME,
    bluesky_post_id VARCHAR(255)
);
```

## Usage

### Running the Bot
```bash
python main.py
```

### Adding Content
Place markdown files in `content/` directory:
```bash
python addContent.py [directory]
```

### Test Mode
Set `TEST_MODE = True` in appSettings.py for testing with shorter intervals.

## Directory Structure
```
├── content/           # Markdown content files
├── blueskyAuth.py    # Bluesky authentication
├── contentManager.py  # Content posting logic
├── main.py           # Main bot script
└── appSettings.py    # Configuration settings
```

## Error Handling
- Logs to console and file
- Failed posts marked in database
- Automatic reconnection for lost connections

## Contributing
Submit pull requests with tests and documentation.

## Known Issues

- Database connections not properly pooled
- No retry mechanism for failed API calls  
- Missing input validation for markdown files
- Test mode needs additional scenarios
- No automatic backups
- Missing rate limiting
- addContent.py duplicates files in Database
- Database needs manual set-up
- Database content themes are not ENUM
- Bot doesn't run in background
- Stop bot not implemented
- Databse Auth issues
- No post engagement log

## License
MIT License
