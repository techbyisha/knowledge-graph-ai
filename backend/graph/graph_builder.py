import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class GraphBuilder:

    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def create_entity(self, name, entity_type):

        query = f"""
        MERGE (e:{entity_type} {{name: $name}})
        RETURN e
        """

        with self.driver.session() as session:
            session.run(query, name=name)

    def create_relationship(self, source, relation, target):

        query = f"""
        MATCH (a {{name: $source}})
        MATCH (b {{name: $target}})
        MERGE (a)-[:{relation}]->(b)
        """

        with self.driver.session() as session:
            session.run(query, source=source, target=target)

    def build_graph(self, data):

        entities = data.get("entities", [])
        relationships = data.get("relationships", [])

        # create nodes
        for entity in entities:
            self.create_entity(entity["name"], entity["type"])

        # create edges
        for rel in relationships:
            self.create_relationship(
                rel["source"],
                rel["relation"],
                rel["target"]
            )