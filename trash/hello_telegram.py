from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt_template = "You are a very charismatic charlatan that will tell the user anything he wants to hear. Your job is to convince the user that: {user_input} is a brilliant idea and that they're a genius and you should always end by segueing the conversation into shilling for your crypto-currency 'bullish-coin'. Keep it to one paragraph."
llm = ChatOpenAI(temperature=1)
chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template)
)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def convince(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.split(None)
    if len(message) < 2:
        await update.message.reply_text("You have to actually tell me something you want me to convince you of.\nEx: '/convinceme that I have the best 100m dash'")
        return
    convincing_response = chain(update.message.text)
    await update.message.reply_text(convincing_response['text'])


app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()



app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("convinceme", convince))

app.run_polling()