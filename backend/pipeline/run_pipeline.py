from backend.ingestion.document_loader import DocumentLoader
from backend.ingestion.entity_extractor import EntityExtractor
from backend.graph.graph_builder import GraphBuilder

def run_pipeline():

    print("Loading documents...")
    loader = DocumentLoader("sample_docs")
    docs = loader.load_documents()

    extractor = EntityExtractor()
    builder = GraphBuilder()

    for doc in docs:
        print(f"Processing: {doc['filename']}")

        print("Extracting entities...")
        data = extractor.extract(doc["content"])

        if data is None:
            print(f"Skipping {doc['filename']} - entity extraction failed")
            continue

        print("Building graph...")
        builder.build_graph(data)

    print("Pipeline completed!")

if __name__ == "__main__":
    run_pipeline()