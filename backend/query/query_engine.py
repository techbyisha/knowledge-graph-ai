import os
import re
from neo4j import GraphDatabase
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def extract_cypher(llm_response: str) -> str:
    """Strip markdown code fences from LLM-generated Cypher."""
    match = re.search(r"```(?:cypher)?\s*(.*?)\s*```", llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return llm_response.strip()

class QueryEngine:

    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def generate_cypher(self, question):
        prompt = f"""
You are an expert in Neo4j Cypher.

Convert the user question into a Cypher query.

Graph schema:
Nodes: Service, Team, Technology, Cloud, Platform
All nodes have a `name` property.

Relationships:
(Service)-[:OWNED_BY]->(Team)
(Service)-[:DEPLOYED_ON]->(Platform)
(Service)-[:HOSTED_IN]->(Cloud)

Rules:
- ALWAYS use case-insensitive match: toLower(n.name) CONTAINS toLower('value')
- Return only the raw Cypher query, no markdown, no explanation.

Example:
Question: Which team owns the authentication service?
Cypher: MATCH (s:Service)-[:OWNED_BY]->(t:Team) WHERE toLower(s.name) CONTAINS toLower('authentication') RETURN t

User Question:
{question}
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def run_query(self, cypher):
        with self.driver.session() as session:
            result = session.run(cypher)
            return [record.data() for record in result]

    def ask(self, question: str) -> list:
        cypher_raw = self.generate_cypher(question)
        cypher = extract_cypher(cypher_raw)
        result = self.run_query(cypher)
        return result