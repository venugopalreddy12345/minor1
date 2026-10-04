import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


def ask_llm(prompt, model="llama3.2:3b"):

    payload = {
        "model": model,

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "stream": False,

        "format": "json",

        "options": {
            "temperature": 0,
            "num_predict": 300
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["message"]["content"]