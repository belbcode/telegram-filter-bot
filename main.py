import dotenv, os, logging
from telegram import Update
from telegram.ext import CommandHandler, Application, ApplicationBuilder
from src.post_init import post_init

# Load environment variables from .env file
dotenv.load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def main():
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).post_init(post_init).build()
    app.run_polling()
    
if __name__ == "__main__":
    main()