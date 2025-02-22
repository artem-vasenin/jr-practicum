from dotenv import load_dotenv
import os

load_dotenv()

GPT_TOKEN = os.getenv("GPT_TOKEN")
GPT_TOKEN_TWO = os.getenv("GPT_TOKEN_TWO")
GPT_TOKEN_THREE = os.getenv("GPT_TOKEN_THREE")
TG_TOKEN = os.getenv("TG_TOKEN")
PROXY = os.getenv("PROXY")
PROXY_THREE = os.getenv("PROXY_THREE")
PROXY_API_TOKEN = os.getenv("PROXY_API_TOKEN")
PROXY_API = os.getenv("PROXY_API")