from .Utils.llm.CallbackHandler import MongoLogger
from langchain import OpenAI
import dotenv

dotenv.load_dotenv()

llm = OpenAI(callbacks=[MongoLogger()])
llm("This is a test. Please work.")