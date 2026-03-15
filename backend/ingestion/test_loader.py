from document_loader import DocumentLoader

loader = DocumentLoader("knowledge-graph-ai/sample_docs")

docs = loader.load_documents()

for doc in docs:
    print("----- Document -----")
    print(doc)