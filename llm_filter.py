from langchain.llms import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser


import dotenv
import random
import string

dotenv.load_dotenv()


def filter_chain(): 

    ### example_strategy

    ### parser_strategy we're using this right now

    class FilterObject:
        filter_id: str = Field(description="ID string for the filter relevant to the message")
        justification: str = Field(description="Why you believe the filter applies to the message.")
    class FilterCollection:
        filters : list[FilterObject] = Field(description="List of filters that apply to the message.")

    prompt_template = """
        You are a content filter.
        Here is a message, {message}; identify if any of the following filters apply to the message.
        {filters}
        {format_instructions}
    """
    model = OpenAI(temperature=0)
    prompt = PromptTemplate.from_template(prompt_template, partial_variables={"format_instructions": parser.get_format_instructions()})
    parser = PydanticOutputParser(pydantic_object=FilterCollection)

    return LLMChain(llm=model, prompt=prompt, output_parser=parser)


class FilterManager:
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.chat_id = update.effective_chat.id
        self.max = 25
        self.filters = {}

    def _repr_filters(self):
        filters = ""
        for filter in self.filters:
            filters += repr(filter)
        return filters

    def add_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(self.filters.keys()) > self.max:
            raise 
        id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        filter = Filter(update, context, id)
        self.filters[id] = filter

    def filter_message(self, update: Update):
        filters = self._repr_filters()
        inputs = {
            "message": update.message.text,
            "filters": filters,
        }
        chain = filter_chain()
        matching_filters = chain(inputs=inputs)
        print(matching_filters)


class Filter:
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE, id: str) -> None:
        self.id = id
        self.text = self._get_filter(update, context)
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
        return f"{self.id} : {self.text}\n"
