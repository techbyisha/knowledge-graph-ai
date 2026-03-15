import os
import json
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

        Return JSON in this format:

        {{
          "entities":[
            {{"name":"", "type":""}}
          ],
          "relationships":[
            {{"source":"", "relation":"", "target":""}}
          ]
        }}

        Text:
        {text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        output = response.choices[0].message.content

        try:
            return json.loads(output)
        except:
            print("Failed to parse JSON")
            print(output)
            return None