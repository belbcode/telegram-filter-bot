from telegram.ext import Application
from telegram import BotCommand
from .Commands.start import start_command, start_bot_command
from .Commands.filter import filter_command, filter_bot_command
from .Commands.list_filters import filter_list_command, filter_list_bot_command, get_filter_list
from .Messages.filter_message import filter_message


async def post_init(application: Application):
    commands = [
        start_bot_command,
        filter_bot_command,
        # filter_list_bot_command
    ]
    await application.bot.set_my_commands(commands)
    application.add_handler(start_command)
    application.add_handler(filter_command)
    # application.add_handlers([filter_list_command, get_filter_list])
    application.add_handler(filter_message)
