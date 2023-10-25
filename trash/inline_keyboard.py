#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
from dotenv import load_dotenv
import os
from llm_filter import FilterManager
import spacy

# Load environment variables from .env file
load_dotenv()

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# class Runtime:
#     def __init__(self) -> None:
#         self.active_chats : Update.effective_chat = []
        

#     def add_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#         self.active_chats.append(update.effective_chat)
#     def chat_lookup(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#         return [chat.id == update.effective_chat.id for chat in self.active_chats][0]

filter_list : FilterManager = []


nlp = spacy.load("en_core_web_sm")

def suggest_commands(text):
    doc = nlp(text)
    suggestions = []

    # Define a list of sample commands or keywords
    commands = ["start", "help", "settings", "search", "info"]

    # Iterate through commands and suggest them if they match tokens in the user's input
    for token in doc:
        for command in commands:
            if token.text.lower() in command:
                suggestions.append(command)

    return suggestions

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    print(user_input)
    # suggestions = suggest_commands(user_input)

    # if suggestions:
    #     update.message.reply_text(f"Suggested commands: {', '.join(suggestions)}")
    # else:
    #     update.message.reply_text("No command suggestions available.")

async def handle_invite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("added memebr")
    for new_member in update.message.new_chat_members:
        print(new_member)
        if new_member.id == context.bot.id:

            filter_list.append(FilterManager(update, context))
            await update.message.reply_text("Hey thanks for adding me!")




async def add_content_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allows the user to set a context filter for incoming messages in a group and receive personal alerts."""
    for filter_manager in filter_list:
        if filter_manager.chat_id == update.effective_chat.id:
            filter_manager.add_filter(update, context)
            await update.message.reply_text(f"Filter added {' '.join(context.args)} ")
        
    # handle_invite(update, context) | add_content_filter(update, context)

async def filter_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allows the user to set a context filter for incoming messages in a group and receive personal alerts."""
    print(update.message.text)
    for filter_manager in filter_list:
        if filter_manager.chat_id == update.effective_chat.id:
            res = filter_manager.filter_message(update)


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Sends a message with three inline buttons attached."""
#     keyboard = [
#         [
#             InlineKeyboardButton("Option 1", callback_data="1"),
#             InlineKeyboardButton("Option 2", callback_data="2"),
#         ],
#         [InlineKeyboardButton("Option 3", callback_data="3")],
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text("Please choose:", reply_markup=reply_markup)


# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query

#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     await query.answer()

#     await query.edit_message_text(text=f"Selected option: {query.data}")


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Displays info on how to use the bot."""
#     await update.message.reply_text("Use /start to test this bot.")


async def show_some_love(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    image_bytes = None
    with open("assets/dumbass2.png", "rb") as image_file:
        image_bytes = image_file.read()

    await update.message.reply_photo(image_bytes, caption="You're a goober ❤️")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

    love_command = CommandHandler("showsomelove", show_some_love)
    filter_command = CommandHandler("filter", add_content_filter)
    invite_handler = MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_invite)
    suggestion_handler = MessageHandler(filters.TEXT, echo)


    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CallbackQueryHandler(button))
    # application.add_handler(CommandHandler("help", help_command))

    application.add_handler(love_command)
    application.add_handler(filter_command)
    application.add_handler(invite_handler)
    application.add_handler(suggestion_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
