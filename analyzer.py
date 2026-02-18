import json
import requests
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"


def call_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["response"]


def analyze_log(log_text: str) -> dict:
    prompt = USER_PROMPT_TEMPLATE.format(log=log_text)

    raw_output = call_llm(prompt)

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {
            "error": "failed_to_parse",
            "raw_output": raw_output,
        }


def main():
    with open("example_logs/failure1.txt") as f:
        log = f.read()

    result = analyze_log(log)

    with open("output/result.json", "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
