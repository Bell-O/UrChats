-- Manual Database Setup for Encrypted Chat App
-- Copy and paste this SQL into your Supabase SQL Editor

-- Enable Row Level Security (RLS) if needed
-- ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-jwt-secret';

-- Create users_public_keys table
CREATE TABLE IF NOT EXISTS public.users_public_keys (
    username TEXT PRIMARY KEY,
    public_key TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create message_log table
CREATE TABLE IF NOT EXISTS public.message_log (
    message_id BIGSERIAL PRIMARY KEY,
    sender_username TEXT NOT NULL,
    recipient_username TEXT NOT NULL,
    ciphertext TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_message_log_recipient 
ON public.message_log(recipient_username);

CREATE INDEX IF NOT EXISTS idx_message_log_sender 
ON public.message_log(sender_username);

CREATE INDEX IF NOT EXISTS idx_message_log_timestamp 
ON public.message_log(timestamp DESC);

-- Enable Row Level Security (optional - for additional security)
ALTER TABLE public.users_public_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.message_log ENABLE ROW LEVEL SECURITY;

-- Create policies to allow all operations (you can make these more restrictive)
CREATE POLICY "Allow all operations on users_public_keys" 
ON public.users_public_keys FOR ALL 
TO authenticated, anon 
USING (true) 
WITH CHECK (true);

CREATE POLICY "Allow all operations on message_log" 
ON public.message_log FOR ALL 
TO authenticated, anon 
USING (true) 
WITH CHECK (true);

-- Insert a test record to verify everything works
INSERT INTO public.users_public_keys (username, public_key, updated_at) 
VALUES ('test_setup', 'test_key_12345', NOW()) 
ON CONFLICT (username) DO NOTHING;

-- Clean up test record
DELETE FROM public.users_public_keys WHERE username = 'test_setup';

-- Verify tables were created successfully
SELECT 'Tables created successfully!' as status,
       'users_public_keys' as table1,
       'message_log' as table2;
