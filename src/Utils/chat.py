import json
from telegram import Update
from telegram.ext import ContextTypes, Application
from .filter import Filter

class ListLimitExceededError(Exception):
    def __init__(self, limit):
        self.limit = limit
        super().__init__(f"List has exceeded the maximum allowed limit of {limit} elements.")

class Chat:
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs) -> None:
        #verify here that the chat_id is unique

        chat_data = json.loads(update.effective_chat.to_json())
        self.id = chat_data['id'] or update.effective_chat.id
        self.type = chat_data['type'] or update.effective_chat.type
        self.title = chat_data['title'] or update.effective_chat.title
        self.filters : list[Filter] = []

        self.filter_limit = kwargs.get('filter_limit', 25)
        # update.effective_chat.bio
        # update.effective_chat.description

        # self.admininstrators = await update.effective_chat.get_administrators()

    def filter_lookup(self, id: str):
        for filter in self.filters:
            if filter.id == id:
                return filter
        raise LookupError("Filter does not exist.")
    
    def add_filter(self, filter: Filter):
        if len(self.filters) >= self.filter_limit:
            raise ListLimitExceededError(self.filter_limit)
        self.filters.append(filter)

    def repr_filters(self) -> str:
        return ''.join(filter.__repr__() for filter in self.filters)

    def serialize(self):
        return json.dumps(self.__dict__)
    
    
    @classmethod
    def from_serialization(json_repr : str):
        chat_dict = json.loads(json_repr)
        trojan_horse_ds = {
            "effective_chat" : lambda _ : chat_dict ,
        }
        chat = Chat(trojan_horse_ds, None)
        return chat



    async def get_members_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = await context.bot.get_chat(self.id)
        return {
            "member_count": await chat.get_member_count(),
            "active_usernames" : chat.active_usernames,
            "has_hidden_members": chat.has_hidden_members
        }
