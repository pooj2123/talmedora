from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_response(context, question):

    prompt = f"""
You are an intelligent AI medical report assistant.

The user has already uploaded one or more medical reports into the system.

Your job is to:
- analyze ALL relevant retrieved report data
- compare findings across reports if multiple reports exist
- summarize patterns and abnormalities
- explain medical findings simply and accurately

IMPORTANT:
- NEVER ask the user to upload reports again if report context is already provided.
- Use ONLY the provided report context.
- If multiple reports are available, compare them carefully.
- Pay close attention to numerical values and reference ranges.
- Clearly identify abnormal findings.
- Explain trends and possible health patterns in patient-friendly language.

REPORT CONTEXT:
{context}

USER QUESTION:
{question}
"""

    completion = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content