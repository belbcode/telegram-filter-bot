from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler
from ..Utils.chat import Chat
from ..Utils.filter import Filter
from ..Utils.runtime_manager import rtm


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Memoizes chat_id and begins tracking messages."""
    product_name = "product_name"
    start_response = f"Thanks for using {product_name}! {product_name} will begin reading this chat's messages."

    chat = Chat(update, context)

    default_filter = Filter(update, context, id="f", override_text="Content unrelated to any of the current filters.")
    chat.add_filter(default_filter)

    try:
        rtm.add_chat(chat)
    except (ValueError):
        await update.message.reply_text("You already used /start if you want to unsubscribe from message monitoring try /stop.")
        return

    await update.message.reply_text(start_response)

start_command = CommandHandler("start", start)
start_bot_command = BotCommand(
    command="start", description="Enables bot to begin reading incoming messages.")
