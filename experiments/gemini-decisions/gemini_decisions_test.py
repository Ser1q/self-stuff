import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"], http_options={"api_version": "v1beta"}
)

result = client.decisions.create(
    model="gemini-decision-1",
    input="I spilled a coffee I ordered from DailyCup onto my sweater.",
    questions={
        "is_dailycup_guilty": {
            "type": "noul",
            "instructions": "Is DailyCup responsible for coffee spilled on the sweater?",
        },
    },
)

answer = result.answers["is_dailycup_guilty"]

print(answer)