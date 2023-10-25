from telegram import Update, BotCommand
import logging
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, Application

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from dotenv import load_dotenv
import os

commands = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="help", description="Get help information"),
    BotCommand(command="settings", description="Change bot settings"),
]

async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(commands)

# Load environment variables from .env file
load_dotenv()

app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).post_init(post_init).build()


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('hi')
    chatid = update.effective_chat.id
    await context.bot.send_message(chat_id=chatid, text=update.message.text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatid = update.effective_chat.id
    await context.bot.send_message(chat_id=chatid, text="Talk to me!")


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"That command does not exist. Try /help to see your options.")

# async def summarize_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_history = update.effective_chat.

echo_handler = MessageHandler(lambda u, c : True, echo)
start_command = CommandHandler('start', start)
caps_command = CommandHandler('caps', caps)

async def init():
    await app.updater.bot.set_my_commands(commands=commands)




if __name__ == '__main__':
    init()
    app.add_handler(start_command)
    app.add_handler(echo_handler)

    app.run_polling()