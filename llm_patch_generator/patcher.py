import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_patch(prompt_json):
    prompt_data = json.loads(prompt_json)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt_data["system"]},
            {"role": "user", "content": prompt_data["user"]}
        ]
    )
    return response['choices'][0]['message']['content']