import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

API_KEY = os.getenv('API_KEY')
