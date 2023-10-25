from telegram.ext import Application
from telegram import BotCommand
from .Commands.start import start_command, start_bot_command
from .Commands.filter import filter_command, filter_bot_command
from .Commands.list_filters import list_filters_command, list_filters_bot_command
from .Messages.filter_message import filter_message


async def post_init(application: Application):
    commands = [
        start_bot_command,
        filter_bot_command,
        list_filters_bot_command
    ]
    await application.bot.set_my_commands(commands)
    application.add_handler(start_command)
    application.add_handler(filter_command)
    application.add_handler(list_filters_command)
    application.add_handler(filter_message)
