-- Check if database exists, create if not
CREATE DATABASE IF NOT EXISTS blueskyAutoContent;

USE blueskyAutoContent;

-- Create content table for storing posts
CREATE TABLE IF NOT EXISTS content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    post_datetime TIMESTAMP NULL,
    theme VARCHAR(50),
    post_number INT,
    retry_count INT DEFAULT 0,
    bluesky_post_id VARCHAR(255)
);

-- Basic indexes for performance
CREATE INDEX IF NOT EXISTS idx_status ON content(status);
CREATE INDEX IF NOT EXISTS idx_theme ON content(theme);
CREATE INDEX IF NOT EXISTS idx_post_datetime ON content(post_datetime);
