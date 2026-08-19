import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

try:
    model_list = client.models.list()

    for model in model_list:
        print(f"Model Name: {model.name}")

except Exception as e:  # noqa: BLE001
    print(f"Failed to fetch models. Error: {e}")

print("\n--- END OF LIST ---")
