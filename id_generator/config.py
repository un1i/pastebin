from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_DSN = os.environ.get('POSTGRES_DSN')

CHECK_IDS_URL = 'http://127.0.0.1:70/check-ids'
