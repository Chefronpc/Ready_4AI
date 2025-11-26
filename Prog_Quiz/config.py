from dotenv import load_dotenv
import os


load_dotenv()

MIN_QUESTIONS: int = 1
MAX_QUESTIONS: int = 30

AI_API_URL = os.getenv("API_URL")
AI_API_KEY = os.getenv("API_KEY")