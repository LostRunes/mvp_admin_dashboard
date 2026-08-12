import os
from dotenv import load_dotenv

# Load from current directory's .env
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(dotenv_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
IMAGEKIT_URL_ENDPOINT = os.getenv("IMAGEKIT_URL_ENDPOINT")

# Validate required variables
missing = []
if not SUPABASE_URL: missing.append("SUPABASE_URL")
if not SUPABASE_KEY: missing.append("SUPABASE_KEY")
if not IMAGEKIT_PUBLIC_KEY: missing.append("IMAGEKIT_PUBLIC_KEY")
if not IMAGEKIT_PRIVATE_KEY: missing.append("IMAGEKIT_PRIVATE_KEY")
if not IMAGEKIT_URL_ENDPOINT: missing.append("IMAGEKIT_URL_ENDPOINT")

if missing:
    raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
