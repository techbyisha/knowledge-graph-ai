import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class EntityExtractor:

    def __init__(self):
        pass

    def extract(self, text):
        prompt = f"""
Extract entities and relationships from the following text.

IMPORTANT RULES:
- Entity types must ONLY be one of: Service, Team, Technology, Cloud, Platform
- Never use any other types like "Organization", "Software", "cloud provider" etc.
- Entity names must be properly capitalized: "Identity Team" not "identity team"
- Return only a JSON object, no markdown, no code fences, no explanation.

Return this exact format:
{{
  "entities": [
    {{"name": "", "type": ""}}
  ],
  "relationships": [
    {{"source": "", "relation": "", "target": ""}}
  ]
}}

Text:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output = response.choices[0].message.content.strip()

        # Strip markdown fences - handle ```json, ```JSON, ``` etc.
        output = re.sub(r"^```[a-zA-Z]*\n?", "", output)  # strip opening fence
        output = re.sub(r"\n?```$", "", output)            # strip closing fence
        output = output.strip()

        try:
            return json.loads(output)
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            print("Raw output:", output)
            return None

