from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler
from mongoengine import Document, DateTimeField, DictField, ListField, IntField, ReferenceField, QuerySetManager, errors
from datetime import datetime



class TelegramChat(Document):
    chat_id = IntField(unique=True, required=True)
    chat_data = DictField(required=True)
    active_commands = ListField(ReferenceField('TelegramCommand'), default=[])
    authorized_users= ListField(IntField)
    joined= DateTimeField(default=datetime.now())
    meta = {
        'indexes': [
            {
                'fields': ['chat_id']
            }
        ]
    }

def store_chat(update: Update):
    chat = update.effective_chat
    tc = TelegramChat(chat_id= chat.id, chat_data=chat.to_dict())
    try:
        tc.save()
    except Exception as e:
        chat = find_chat(update)
        if not chat:
            raise e
    return tc

def find_chat(update: Update):
    _id = update.effective_chat.id
    chat = TelegramChat.objects(chat_id=_id)
    if len(chat) == 1: print (chat);return chat
    elif len(chat) > 1: return chat ## need to handle this possibility
    return None