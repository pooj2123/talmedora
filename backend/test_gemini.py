from google import genai

client = genai.Client(
    api_key="AIzaSyD4zaRLQL6Ugg2YoV7qCIbu7OTdPuvwMaw"
)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="hello"
)

print(response.text)