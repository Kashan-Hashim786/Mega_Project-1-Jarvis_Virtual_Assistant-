from openai import OpenAI
client = OpenAI(
    api_key="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"
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistent named jarvis skilled in general tasks like alexa."},
        {
            "role": "user",
            "content": "What is coding."
        }
    ]
)

print(completion.choices[0].message)