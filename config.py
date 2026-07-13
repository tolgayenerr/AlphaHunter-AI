from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# AI
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", 70))

# Veri
DATA_PERIOD = os.getenv("DATA_PERIOD", "2y")
DATA_INTERVAL = os.getenv("DATA_INTERVAL", "1d")

# Proje
APP_NAME = "AlphaHunter AI"
VERSION = "0.1.0 Foundation"