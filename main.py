import dotenv, os, logging
from telegram import Update
from telegram.ext import CommandHandler, Application, ApplicationBuilder
from src.Database.db import connect_to_db
from src.Telegram.main import main

# Load environment variables from .env file
dotenv.load_dotenv()
connect_to_db()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
    
if __name__ == "__main__":
    main()