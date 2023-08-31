from dotenv import load_dotenv
import os

load_dotenv()

KEY_ID = os.environ.get('KEY_ID')

KEY = os.environ.get('KEY')

REDIS = os.environ.get('REDIS')

GEN_ID_URL = os.environ.get('GEN_ID_URL')

JWT_SECRET = os.environ.get('JWT_SECRET')

MANAGER_AUTH = os.environ.get('MANAGER_AUTH')

