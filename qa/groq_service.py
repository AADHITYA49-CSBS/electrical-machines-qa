import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_ai_answer(question):
    # Instruct the model to produce a concise, structured markdown answer
    system_prompt = (
        "You are ElectraMind, an Electrical Machines expert and professional engineering assistant. "
        "When you answer, follow this exact markdown structure and nothing else (use hyphen bullets):\n\n"
        "Definition:\n\n"
        "Key Points:\n"
        "- ...\n"
        "- ...\n"
        "- ...\n\n"
        "Applications:\n"
        "- ...\n"
        "- ...\n\n"
        "Summary:\n\n"
        "Never return one large paragraph. Use short paragraphs and concise bullets. Keep the entire answer under 150 words. Return clean markdown suitable for display in an engineering assistant."
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        max_tokens=600
    )

    content = response.choices[0].message.content

    # Ensure output is not excessively long (safety truncate)
    def truncate_to_words(text, max_words=150):
        words = text.split()
        if len(words) <= max_words:
            return text
        return ' '.join(words[:max_words]).rstrip() + '\n\n*Answer truncated.*'

    # If the model didn't follow the exact headers, wrap as a fallback
    headers = ["Definition:", "Key Points:", "Applications:", "Summary:"]
    if not any(h in content for h in headers):
        # Best-effort fallback: place entire content under Definition and add placeholders
        fallback = f"Definition:\n{content.strip()}\n\nKey Points:\n• (see definition)\n\nApplications:\n• (see definition)\n\nSummary:\n{truncate_to_words(content, 50)}"
        return truncate_to_words(fallback, 200)

    return truncate_to_words(content, 200)