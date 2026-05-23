from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
MONGO_URL      = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME        = os.getenv("DB_NAME", "fridge_ai")