from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler
from ..Utils.runtime_manager import rtm
from ..Utils.filter import Filter

async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = rtm.chat_lookup(update.effective_chat.id)
    if chat == None:
        await update.message.reply_text("Filters not yet enabled on this chat. Try /start")
        return
    reply = "".join(filter.__repr__() for filter in chat.filters)
    await update.message.reply_text(reply)

list_filters_command = CommandHandler("listfilters", list_filters)
list_filters_bot_command = BotCommand("listfilters", "List all currently active filters")