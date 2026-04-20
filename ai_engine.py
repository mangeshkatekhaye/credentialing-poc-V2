import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_info(text):
    prompt = f"""
    Extract the following details from the given document:

    - Full Name
    - Email
    - Phone Number
    - Skills (list of strings)
    - Total Experience (in years)

    Return ONLY valid JSON.
    Do NOT include ``` or any extra text.

    Document:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert document parser."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content