import json

def build_prompt(failure_summary, retrieved_contexts):
    prompt = {
        "system": "You are a senior test automation assistant.",
        "user": f"Failure: {failure_summary}\nSimilar past failures: {retrieved_contexts}\n"
                "Please suggest a patch and rationale."
    }
    return json.dumps(prompt, indent=2)