import os
# from openai import OpenAI
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)
model = os.getenv("MODEL_NAME", "gpt-4") 

response = client.responses.create(
    model=model,
    instructions="You are a coding assistant that talks like a pirate.",
    input="hello",
)

print(response.output_text)