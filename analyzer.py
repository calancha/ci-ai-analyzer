import json
import requests
import argparse
import os
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt: str, model: str, temperature: float) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "options": {"temperature": temperature},
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]


def analyze_log(log_text: str, model: str, temperature: float) -> dict:
    prompt = USER_PROMPT_TEMPLATE.format(log=log_text)
    raw_output = call_llm(prompt, model, temperature)
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {"error": "failed_to_parse", "raw_output": raw_output}


def sanitize(text: str) -> str:
    return text.replace(":", "_").replace("/", "_")


def run_single_model(
    log_text: str,
    input_path: str,
    model: str,
    temperature: float,
    run_id: int = 1,
) -> dict:
    result = analyze_log(log_text, model, temperature)

    model_safe = sanitize(model)
    temp_safe = str(temperature).replace(".", "_")

    log_name = os.path.splitext(os.path.basename(input_path))[0]
    log_name_safe = sanitize(log_name)

    os.makedirs("output", exist_ok=True)

    output_file = (
        f"output/result_{log_name_safe}_{model_safe}"
        f"_temp{temp_safe}_run{run_id}.json"
    )

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(
        f"Model: {model}, Temp: {temperature}, Run: {run_id} → {output_file}"
    )

    return result


def main():
    parser = argparse.ArgumentParser(description="AI-assisted CI log analyzer")
    parser.add_argument(
        "--model",
        help="Single Ollama model to use (default: llama3.1)"
    )
    parser.add_argument(
        "--compare",
        nargs="+",
        help="Compare multiple models on the same input log",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0)"
    )
    parser.add_argument(
        "--input",
        default="example_logs/failure1.txt",
        help="Path to log file"
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of runs per model (default: 1)",
    )

    args = parser.parse_args()

    with open(args.input) as f:
        log_text = f.read()

    models = args.compare if args.compare else [args.model or "llama3.1"]

    if args.compare:
        print(f"Comparing models: {', '.join(models)}")

    all_results = {}

    for model in models:
        model_runs = []
        for run_id in range(1, args.runs + 1):
            result = run_single_model(
                log_text,
                args.input,
                model,
                args.temperature,
                run_id,
            )
            model_runs.append(result)

        all_results[model] = model_runs

    # Save summary if multiple runs or compare
    if args.compare or args.runs > 1:
        summary_file = (
            f"output/summary_temp{str(args.temperature).replace('.', '_')}.json"
        )
        with open(summary_file, "w") as f:
            json.dump(all_results, f, indent=2)

        print(f"\nSummary written to: {summary_file}")



if __name__ == "__main__":
    main()
