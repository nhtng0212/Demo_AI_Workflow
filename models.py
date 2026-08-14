import os

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the standard Google GenAI client
client = genai.Client(api_key=api_key)

print("--- FETCHING AVAILABLE GEMINI MODELS ---\n")

try:
    # Call the API to get a list of all models
    model_list = client.models.list()

    # Iterate through the list and print the model names
    for model in model_list:
        print(f"Model Name: {model.name}")

except Exception as e:  # noqa: BLE001
    # Catch and print any connection or authentication errors
    print(f"Failed to fetch models. Error: {e}")

print("\n--- END OF LIST ---")
