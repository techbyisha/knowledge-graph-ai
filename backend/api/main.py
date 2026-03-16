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

    answer = None

    if result and len(result) > 0:
        record = result[0]              # first result
        node = list(record.values())[0] # get node dictionary
        answer = node.get("name")       # extract name

    return {
        "question": request.question,
        "answer": answer
    }