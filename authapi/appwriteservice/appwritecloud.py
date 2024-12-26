import os
from appwrite.client import Client
from dotenv import load_dotenv

load_dotenv()

APPWRITE_API_KEY = os.getenv('APPWRITE_API_KEY')
APPWRITE_PROJECT_ID = os.getenv('APPWRITE_PROJECT_ID')
APPWRITE_BASE_URL = os.getenv('APPWRITE_BASE_URL')
APPWRITE_DB_ID = os.getenv('APPWRITE_DB_ID')
APPWRITE_COLLECTION_ID = os.getenv('APPWRITE_COLLECTION_ID')

client = Client()

(client
  .set_endpoint(APPWRITE_BASE_URL) # Your API Endpoint
  .set_project(APPWRITE_PROJECT_ID) # Your project ID
  .set_key(APPWRITE_API_KEY) # Your secret API key
)


