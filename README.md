# telegram-filter-bot
## This is a telegram bot that can enables you to set filters on Telegram chats.
## At the moment, Chats are stored in memory so every time you restart the server it loses its memory.

To get started, clone this repo and set a .env file.

```.env
OPENAI_API_KEY="..."
TELEGRAM_TOKEN="..."

```
### Get your OpenAI API Key @ https://platform.openai.com/
### Instructions for obtaining a Telegram Bot Token @ https://core.telegram.org/bots/tutorial#getting-ready

Once your .env file is set up you simply need to run in the terminal.
```bash
$ python3 main.py
```

Invite the chatbot to a group, and initialize it with /start.
Then you can add filters with /filter.
Then every message 
New features added daily.
