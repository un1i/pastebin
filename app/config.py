from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_DSN = os.environ.get('POSTGRES_DSN')

KEY_ID = os.environ.get('KEY_ID')

KEY = os.environ.get('KEY')

GEN_ID_URL = 'http://127.0.0.1:70'
