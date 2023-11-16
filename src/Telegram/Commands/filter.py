from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler
from .ExportCommand import ExportCommand
from ..setup import RTM
from ..Utils.filter import Filter
import random, string

async def filtercommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    chat = RTM.chat_lookup(update.effective_chat.id)
    if chat == None:
        await update.message.reply_text("Filters not yet enabled on this chat. Try /start")
        return
    id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    new_filter = Filter(update, context, id)
    chat.filters.append(new_filter)

    await context.bot.send_message(update.effective_chat.id, text= f"We'll start checking messages for content that matches {' '.join(context.args)}")

filter = ExportCommand(CommandHandler("filter", filtercommand), BotCommand('filter', "Add an AI powered content filter."))

