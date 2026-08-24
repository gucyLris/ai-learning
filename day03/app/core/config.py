import os

from dotenv import load_dotenv

load_dotenv()


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


DEEPSEEK_BASE_URL = "https://api.deepseek.com"


DEEPSEEK_MODEL = "deepseek-chat"


if not DEEPSEEK_API_KEY:

    raise ValueError("DEEPSEEK_API_KEY 未配置")
