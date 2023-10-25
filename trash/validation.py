from telegram import Update
from telegram.ext import ContextTypes


def is_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return update.effective_user.is_bot
