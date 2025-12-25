from google import generativeai as genai
from google.generativeai import types


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)