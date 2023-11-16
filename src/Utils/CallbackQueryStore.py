from telegram import Update
from random_string import random_string
class CallbackQueryStore:
    ## Trivial Global Dict
    ## Let's you store and retrieve data in between CallbackQueries
    def __init__(self, **kwargs) -> None:
        self.storage = dict()
        keylen = kwargs.get('keylen', 12) ## This can max be 64
        if keylen > 64 or keylen < 8:
            raise ValueError("Keylen must be a value between 8 and 64") ## 8 to avoid map collisions, 64 due to the byte limit of callback_data.
    def store(self, payload_object: any):
        key = random_string(self.keylen)
        self.storage[key] = payload_object 
        return key
    def retrieve(self, id: str):
        payload_object = self.storage.get(id, None) 
        if payload_object == None:
            raise RetrievalError(f"Failed to retrieve {id} from CallbackQueryStore")
        del self.storage[id] ## No longer need the payload.
        return payload_object

def handle_retrieval_error(update: Update):
    update.callback_query.answer()
    update.callback_query.message.edit_text("There was an error making this request, probably a timeout. Try again.")

class RetrievalError(BaseException):
    def resolve(update: Update):
        update.callback_query.answer()  
        update.callback_query.message.edit_text("There was an error making this request. Try again.")