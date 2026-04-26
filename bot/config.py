import logging
import os

from dotenv import load_dotenv


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = 1888074242
STATS_FILE = "stats.json"
