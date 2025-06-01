
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GEMINI_API_KEY")


import openai

def chat_with_agent(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        msg = input("You: ")
        if msg.lower() in ['exit', 'quit']:
            break
        print("Agent:", chat_with_agent(msg))