from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_DSN = os.environ.get("POSTGRES_DSN")