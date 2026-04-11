from supabase import create_client

SUPABASE_URL = "API URL"
SUPABASE_KEY = "SECRET KEY" 

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

