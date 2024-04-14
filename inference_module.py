import requests
import re
import json
import dotenv
import os
import time

dotenv.load_dotenv(".env")

def extract_json(raw):
    cleaned_json = re.search(r"\s?({.*})\s?", raw, re.DOTALL).group(1)
    cleaned_json = json.loads(cleaned_json)
    return cleaned_json

def llm_inference(prompt):
    """
    Accepts a prompt and returns the response
    Doesnt accept seperate system prompt, only user prompt
    """

    provider = "google"
    model = "gemini-1.5-pro"

    if provider == "together":
        api_key = os.getenv("TOGETHER_API_KEY")
        endpoint = 'https://api.together.xyz/inference'

        if model == "mixtral":
            response = requests.post(
                url=endpoint,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                    "prompt": f"[INST] {prompt} [/INST]",
                    "max_tokens": 16000,
                    "temperature": 0.2,
                }, )

            if response.status_code == 200:
                content = response.json()
                return content["output"]["choices"][0]["text"]
            else:
                raise Exception(f"Request failed with status code {response.status_code}")
            
    if provider == "google":
        if model == "gemini-1.5-pro":
            api_key = os.getenv("GEMINI_API_KEY")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}

            parts = []
            parts.append({"text": prompt})

            payload = {
                "contents": [
                    {
                        "parts": parts
                    }
                ],
                "generationConfig": {
                    "temperature": 0.4,
                    "topK": 32,
                    "topP": 1,
                    "maxOutputTokens": 4096,
                    "stopSequences": []
                }
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                content = response.json()
                return content["candidates"][0]["content"]["parts"][0]["text"]
            elif response.status_code == 429:
                time.sleep(1)
                return llm_inference(prompt)
            else:
                raise Exception(f"Request failed with status code {response.status_code}")
            
if __name__ == "__main__" :
    print(llm_inference("what is the meaning of life"))