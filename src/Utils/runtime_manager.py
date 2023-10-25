from .chat import Chat
class RuntimeManager:
    chats: list[Chat] = []

    def chat_lookup(self, id: int):
        """Looks up stored chats by Id if doesn't exist returns None"""
        for chat in self.chats:
            if id == chat.id:
                return chat
        return None
    
    def add_chat(self, chat: Chat):
        if self.chat_lookup(chat.id) == None:
            self.chats.append(chat)
        else:
            raise ValueError("Chat has already been intialized.")


rtm = RuntimeManager()