import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_ai_answer(question):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content":
                "You are an Electrical Machines expert. "
                "Answer questions about transformers, motors, generators, alternators and electrical machines."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content