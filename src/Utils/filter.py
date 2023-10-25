from telegram import Update
from telegram.ext import ContextTypes

class Filter:
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE, id: str, **kwargs) -> None:
        self.id = id
        self.text = kwargs.get('override_text', None) or self._get_filter(update, context)
        self.subscribers = [update.effective_user.id]
        self.chat_id = update.effective_chat.id

    def _get_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            filter_text = ' '.join(context.args)
        except (IndexError):
            update.effective_chat.send_message(
                "You need to specify the type of message you want to message")
            raise ValueError("Missing an argument for filter_text")
        return filter_text

    def subscribe(self, update: Update):
        self.subscribers.append(update.effective_user.id)

    def __repr__(self) -> str:
        return f"(filter_id) {self.id} : {self.text}\n"