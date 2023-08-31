from dotenv import load_dotenv
import os

load_dotenv()

CHECK_IDS_URL = os.environ.get('CHECK_IDS_URL')

REDIS = os.environ.get('REDIS')


