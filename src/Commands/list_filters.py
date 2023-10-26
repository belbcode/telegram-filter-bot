from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from ..Utils.runtime_manager import rtm
from ..Utils.filter import Filter


# class OptionHandler:
#     def __init__(self, option_list: list(dict["option_text": str, "option_callback": lambda **kwargs: None])) -> None:
#         self.keyboard_options = []
#         for opt in option_list:
#             self.keyboard_options.append(InlineKeyboardButton(opt["option_text"], opt["callback"]))

class Pattern:
    def __init__(self, pattern: str, payload: str):
        self.pattern = pattern
        self.payload = payload
def pattern_matcher(match_value: str):
    return lambda p:  print(p) or True



async def filter_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = rtm.chat_lookup(update.effective_chat.id)
    if chat == None:
        await update.message.reply_text("Filters not yet enabled on this chat. Try /start")
        return

    keyboard = [InlineKeyboardButton(
        filter.text, callback_data=Pattern("filterlist", filter)) for filter in chat.filters]
    reply_markup = InlineKeyboardMarkup([keyboard])

    await update.message.reply_text("Filter List", reply_markup=reply_markup)


async def handle_filter_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat = rtm.chat_lookup(query.message.chat.id)
    relevant_filter = chat.filter_lookup(query.data)
    keyboard = [
        InlineKeyboardButton('Delete', callback_data=''),
        InlineKeyboardButton('Edit', callback_data=''),
        InlineKeyboardButton(
            f"{'Deactivate' if relevant_filter.active else 'Activate'}", callback_data='')
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.edit_message_text(text=f"Selected option:", reply_markup=reply_markup)

filter_list_command = CommandHandler("filterlist", filter_list)
filter_list_bot_command = BotCommand(
    "filterlist", "List all currently active filters")
get_filter_list = CallbackQueryHandler(handle_filter_list, pattern=pattern_matcher("filterlist"))

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
