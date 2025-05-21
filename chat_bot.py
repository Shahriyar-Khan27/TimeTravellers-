import requests

# Your Groq API Key (use env vars in production)
api_key = "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"
groq_url = "https://api.groq.com/openai/v1/chat/completions"

def ChatWIthLLM(question):
    with open("data.txt") as f:
        data = f.read()

    prompt = f"""
System: You are an AI assistant tasked with giving me output based on the context I provide. If it isn't present
in context, say `I don't know`. If the question is of small talk type like `hi`, `how are you`, `thank you`, then you should reply appropriately instead of saying `I don't know`. The answer should be based on facts shared in <context> tag while the question is
shared in <question> tag.

Human: 
<context>
{data}
</context>

<question>
{question}
</question>

Ensure that response is based upon the context.

Response:
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(groq_url, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        print(reply)
        return reply
    else:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
