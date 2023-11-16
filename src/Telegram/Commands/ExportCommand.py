from telegram.ext import CommandHandler, Application
from telegram import BotCommand

class ExportCommand:

    def __init__(
            self,
            CommandHandler: CommandHandler,
            BotCommand: BotCommand,
            group: int = 0
        ) -> None:
        self.CommandHandler = CommandHandler
        self.BotCommand = BotCommand
        self.group = group

    def __str__(self) -> str:
        return "ExportCommand"

        
    def add_to_application(self, app: Application, command_list: list[BotCommand]):
        app.add_handler(self.CommandHandler, group=self.group)
        command_list.append(self.BotCommand)

    def expose(self) -> (CommandHandler, BotCommand):
        return (self.CommandHandler, self.group, self.BotCommand)
        
