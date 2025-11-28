# config.py
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("OPEN_AI_ENDPOINT_5")
api_key = os.getenv("OPEN_AI_KEY_5")
api_version = "2025-03-01-preview"
deployment = "gpt-5.1"