from fastapi import FastAPI
from pydantic import BaseModel
from backend.query.query_engine import QueryEngine

app = FastAPI()

engine = QueryEngine()


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Knowledge Graph API is running"}


@app.post("/query")
def query_graph(request: QueryRequest):

    result = engine.ask(request.question)

    return {
        "question": request.question,
        "result": result
    }