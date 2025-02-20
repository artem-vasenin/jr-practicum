from dotenv import load_dotenv
import os

load_dotenv()

GPT_TOKEN = os.getenv("GPT_TOKEN")
GPT_TOKEN_TWO = os.getenv("GPT_TOKEN_TWO")
TG_TOKEN = os.getenv("TG_TOKEN")
PROXY = os.getenv("PROXY")