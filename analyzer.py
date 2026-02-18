import json
import requests
import argparse
import os

from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt: str, model: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["response"]


def analyze_log(log_text: str, model: str) -> dict:
    prompt = USER_PROMPT_TEMPLATE.format(log=log_text)

    raw_output = call_llm(prompt, model)

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {
            "error": "failed_to_parse",
            "raw_output": raw_output,
        }


def sanitize_model_name(model: str) -> str:
    return model.replace(":", "_").replace("/", "_")


def main():
    parser = argparse.ArgumentParser(description="AI-assisted CI log analyzer")
    parser.add_argument(
        "--model",
        default="llama3.1",
        help="Ollama model to use (default: llama3.1)",
    )
    parser.add_argument(
        "--input",
        default="example_logs/failure1.txt",
        help="Path to log file",
    )

    args = parser.parse_args()

    model = args.model

    with open(args.input) as f:
        log = f.read()

    result = analyze_log(log, model)

    os.makedirs("output", exist_ok=True)

    model_safe = sanitize_model_name(model)
    output_file = f"output/result_{model_safe}.json"

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nModel: {model}")
    print(f"Output written to: {output_file}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
