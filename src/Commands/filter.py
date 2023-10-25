from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler
from ..Utils.runtime_manager import rtm
from ..Utils.filter import Filter
import random, string

async def filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    chat = rtm.chat_lookup(update.effective_chat.id)
    if chat == None:
        await update.message.reply_text("Filters not yet enabled on this chat. Try /start")
        return
    id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    new_filter = Filter(update, context, id)
    chat.filters.append(new_filter)

    await context.bot.send_message(update.effective_chat.id, text= f"We'll start checking messages for content that matches {' '.join(context.args)}")


filter_command = CommandHandler("filter", filter)

filter_bot_command = BotCommand('filter', "Add an AI powered content filter.")