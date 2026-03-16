import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


def sanitize_label(label: str) -> str:
    """Convert 'cloud provider' → 'CloudProvider' for valid Neo4j labels."""
    return label.strip().title().replace(" ", "")

def sanitize_relation(relation: str) -> str:
    """Convert 'owned by' → 'OWNED_BY' for valid Neo4j relationship types."""
    return relation.strip().upper().replace(" ", "_")


class GraphBuilder:

    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def create_entity(self, name, entity_type):
        label = sanitize_label(entity_type)
        query = f"""
        MERGE (e:{label} {{name: $name}})
        RETURN e
        """
        with self.driver.session() as session:
            session.run(query, name=name.strip().title())  # ← normalize name casing

    def create_relationship(self, source, relation, target):
        rel_type = sanitize_relation(relation)
        query = f"""
        MATCH (a {{name: $source}})
        MATCH (b {{name: $target}})
        MERGE (a)-[:{rel_type}]->(b)
        """
        with self.driver.session() as session:
            session.run(query, source=source.strip().title(),  # ← normalize
                               target=target.strip().title())  # ← normalize

    def build_graph(self, data):
        entities = data.get("entities", [])
        relationships = data.get("relationships", [])

        for entity in entities:
            print(f"  Creating entity: {entity['name']} ({entity['type']})")
            self.create_entity(entity["name"], entity["type"])

        for rel in relationships:
            print(f"  Creating relationship: {rel['source']} -[{rel['relation']}]-> {rel['target']}")
            self.create_relationship(rel["source"], rel["relation"], rel["target"])