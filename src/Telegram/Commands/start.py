from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler
from ...Database.Models.Telegram_Chat import TelegramChat
from mongoengine import NotUniqueError
from logging import log



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Stores Chat into database"""
    product_name= "Semantic"
    response = f"Thanks for using {product_name} Bot! See what we can do with /help."

    # Clean data
    chat = update.effective_chat
    chat_data = chat.to_dict()
    del chat_data['id']

    tc = TelegramChat(chat_id=chat.id, chat_data=chat_data)

    try:
        tc.save()
    except NotUniqueError:
        response ="You already enabled the bot on this chat. See what we can do with /help."
    except Exception as e:
        response = f"There is an issue with your request. We'll try to fix it as soon as possible"
        log(level=0, message=e)
    finally:
        await update.message.reply_text(response)

command = CommandHandler("start", start)
bot_command = BotCommand(command="start", description="Enables bot to begin reading incoming messages.")
