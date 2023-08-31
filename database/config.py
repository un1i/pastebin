from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_DSN = os.environ.get('POSTGRES_DSN')

SYNC_DSN = os.environ.get('SYNC_DSN')

POSTGRES_DSN_TEST = os.environ.get('POSTGRES_DSN_TEST')