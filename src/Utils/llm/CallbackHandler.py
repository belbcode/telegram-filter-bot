from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler, AsyncCallbackHandler
from typing import Dict, Any, List, Optional, Union
from langchain.schema.messages import BaseMessage
from langchain.schema.output import LLMResult
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from pymongo.database import Database
from langchain.embeddings.base import Embeddings
import bson
from langchain.embeddings import OpenAIEmbeddings

from pymongo import MongoClient

client = MongoClient("localhost", 27017)

semantic_db = client.semantic

def embed(text: str, embedder: Embeddings):
    return embedder.embed_query(text)

class MongoModel(BaseModel):

    collection: str
    run_id: UUID

    def serialize(self):
        print(self.dict(), {'run_id': bson.Binary.from_uuid(self.run_id)} )
        return self.dict() | {'run_id': bson.Binary.from_uuid(self.run_id)} 
    def record(self) -> InsertOneResult:
        return semantic_db[self.collection].insert_one(self.serialize())

class LLMRequest(MongoModel):
    prompts: List[str]
    serialized: Dict[str, Any]

class ChatRequest(MongoModel):
    messages: List[List[BaseMessage]]
    serialized: Dict[str, Any]
    run_id: UUID

class LLMResponse(MongoModel):
    LLMResult: LLMResult
    run_id: UUID

class Embedding(MongoModel):
    embeddings: List[list[float]]
    request_id: int
    embedder: Dict[str, Any]


class MongoLogger(BaseCallbackHandler):


    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], run_id, **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        print(serialized, prompts, run_id, kwargs.get('run_id'))
        llmrequest = LLMRequest(collection="llm_request", serialized=serialized, prompts=prompts, run_id=run_id)
        result = llmrequest.record()
        embedder = OpenAIEmbeddings()
        embeddings = Embedding(run_id=result.inserted_id)
        embeddings.record()


    def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]],  **kwargs: Any) -> Any:
        print(serialized, messages, kwargs.get('run_id'))

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        print(response, kwargs.get('run_id'))

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM ends running."""

    def on_llm_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM errors."""





from langchain import OpenAI
import dotenv

dotenv.load_dotenv()

llm = OpenAI(callbacks=[MongoLogger()])
llm("This is a test. Please work.")