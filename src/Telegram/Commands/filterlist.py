from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from ..setup import RTM
from ..Utils.CallbackQueryStore import CallbackQueryStore
CBS = CallbackQueryStore()
# class OptionHandler:
#     def __init__(self, option_list: list(dict["option_text": str, "option_callback": lambda **kwargs: None])) -> None:
#         self.keyboard_options = []
#         for opt in option_list:
#             self.keyboard_options.append(InlineKeyboardButton(opt["option_text"], opt["callback"]))


class Pattern:
    def __init__(self, pattern: str, payload: str):
        self.pattern = pattern
        self.payload = payload


def pattern_match(match_value: str, parse_function: lambda x: str):
    return lambda callback_data: match_value == parse_function(callback_data)


async def filter_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = RTM.chat_lookup(update.effective_chat.id)
    if chat == None:
        await update.message.reply_text("Filters not yet enabled on this chat. Try /start")
    else:
        keyboard = [InlineKeyboardButton(filter.text, f"filteroptions:{filter.id}") for filter in chat.filters]
        reply_markup = InlineKeyboardMarkup([keyboard])
        await update.message.reply_text("Filter List", reply_markup=reply_markup)


def parse_callback_data(callback_data: str):
    pattern, payload = callback_data.split(":")
    return {
        "pattern": pattern,
        "payload": payload
    }

def match_function(pattern: str, parser_function):
    return lambda callback_data: parser_function(callback_data)['pattern'] == pattern

async def filter_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat = RTM.chat_lookup(query.message.chat.id)
    if chat == None:
        await query.answer()
        await query.edit_message_text("There has been an error locating your chat. You may have timed out or your group may have been migrated.")
    else:
        relevant_filter = chat.filter_lookup(query.data)
        keyboard = [
            InlineKeyboardButton('Delete', callback_data='delete'),
            InlineKeyboardButton('Edit', callback_data='edit'),
            InlineKeyboardButton(
                f"{'Deactivate' if relevant_filter.active else 'Activate'}", callback_data=f"toggle")
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.answer()
        await query.edit_message_text(text=f"Selected option:", reply_markup=reply_markup)

async def filter_option_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat = RTM.chat_lookup(query.message.chat.id)
    if chat == None:
        await query.answer()
        await query.edit_message_text("There has been an error locating your chat. You may have timed out or your group may have been migrated.")
    else:
        parsed_data = parse_callback_data(query.data)
        filter_id = parsed_data['payload']
        filter = chat.filter_lookup(filter_id)
        query.answer()

        match filter_id:
            case 'delete':
                chat.delete_filter(filter_id)
                query.edit_message_text("The filter '{filter.text}' was deleted.")
            case 'edit':
                query.edit_message_text(":(")
            case 'toggle':
                filter.toggle()
                query.edit_message_text(f"The filter '{filter.text}' was {'activated' if filter.active else 'deactovated'}.")
    



filter_list_command = CommandHandler("filterlist", filter_list)
filter_list_bot_command = BotCommand("filterlist", "List all currently active filters")

get_filter_option = CallbackQueryHandler(filter_options, pattern=match_function("filteroptions", parse_callback_data))



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
