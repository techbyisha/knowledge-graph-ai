from backend.query.query_engine import QueryEngine

engine = QueryEngine()

question = "Which team owns the authentication service?"
result = engine.ask(question)

print("\nAnswer:", result)