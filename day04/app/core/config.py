import os

from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL")

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY 未配置")
