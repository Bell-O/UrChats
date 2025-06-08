-- Create users_public_keys table
CREATE TABLE IF NOT EXISTS users_public_keys (
    username TEXT PRIMARY KEY,
    public_key TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create message_log table  
CREATE TABLE IF NOT EXISTS message_log (
    message_id SERIAL PRIMARY KEY,
    sender_username TEXT NOT NULL,
    recipient_username TEXT NOT NULL,
    ciphertext TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_message_log_recipient ON message_log(recipient_username);
CREATE INDEX IF NOT EXISTS idx_message_log_sender ON message_log(sender_username);
CREATE INDEX IF NOT EXISTS idx_message_log_timestamp ON message_log(timestamp);

-- Insert a test record to verify tables work
INSERT INTO users_public_keys (username, public_key, updated_at) 
VALUES ('test_user', 'test_key', NOW()) 
ON CONFLICT (username) DO NOTHING;

-- Clean up test record
DELETE FROM users_public_keys WHERE username = 'test_user';

SELECT 'Tables created successfully!' as status;
