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


def filter_chain(): #llm_options: dict 

    ### example_strategy

    ### parser_strategy we're using this right now

    class FilterObject(BaseModel):
        filter_id: str = Field(description="id string for the filter relevant to the message")
        justification: str = Field(description="Why you believe the filter applies to the message.")
    class FilterCollection(BaseModel):
        filters : list[FilterObject] = Field(description="List of filters that apply to the message.")

    prompt_template = """
        You receive a message from a message-group and list which filters apply to the message.
        Do NOT list filters that are irrelevant to the message.
        --MESSAGE--
        {message}
        --FILTERS--
        {filters}
        --FORMAT INSTRUCTIONS--
        {format_instructions}
    """
    prompt_template = """
        You are a content manager. Have a look at the following content filters.
        --FILTERS--
        {filters}
        Select the filters which apply to the following message.
        For a filter to apply to a message, the filter must also be able to serve as an accurate description the message.
        Simply containing information related to the filter is not enough. 
        --MESSAGE--
        {message}
        --FORMAT INSTRUCTIONS--
        {format_instructions}
    """
    model = OpenAI(temperature=0)
    parser = PydanticOutputParser(pydantic_object=FilterCollection)
    prompt = PromptTemplate.from_template(prompt_template, partial_variables={"format_instructions": parser.get_format_instructions()})
    return LLMChain(llm=model, prompt=prompt, output_parser=parser)
