import os
from document_loader import DocumentLoader

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sample_docs_dir = os.path.join(base_dir, "sample_docs")

loader = DocumentLoader(sample_docs_dir)

docs = loader.load_documents()

for doc in docs:
    print("----- Document -----")
    print(doc)