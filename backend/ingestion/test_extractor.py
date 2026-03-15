import os
from document_loader import DocumentLoader
from entity_extractor import EntityExtractor

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sample_docs_dir = os.path.join(base_dir, "sample_docs")

loader = DocumentLoader(sample_docs_dir)
docs = loader.load_documents()

extractor = EntityExtractor()

for doc in docs:

    print("\n---- Document ----\n")
    print(doc["content"])

    result = extractor.extract(doc["content"])

    print("\n---- Extracted Graph ----\n")
    print(result)