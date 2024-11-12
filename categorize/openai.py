import requests
import json
import re
from config import OPENAI_API_KEY, token_encoding


def get_token_count(text):
    token_count = 0
    try:
        token_count = len(token_encoding.encode(text))
    except Exception as e:
        print(f"Error: {e}")
    return token_count


def get_completions_openai(text):
    print("text: ", text)
    prompt = f"""Generate category breadcrumb that is minimum 3 levels deep for the following text: {text}"""

    token_count = get_token_count(prompt)
    print(f"Token count: {token_count}")

    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    data = {
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': 256,
        'temperature': 0
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    aihub_completions_resp = requests.post(OPENAI_API_URL, json=data, headers=headers)
    try:
        openai_completions_resp = aihub_completions_resp.json()
        response = openai_completions_resp['choices'][0]['message']['content']
        crumb = re.search(r"\*\*(.*?)\*\*", response).group(1)
        crumb = crumb.replace("Home >", '', 1)
        return crumb
    except Exception as e:
        print(f"Error: {e}")

def get_embeddings_openai(text, attempt=0):
    OPENAI_API_URL = "https://api.openai.com/v1/embeddings"

    data = {
        "input": text,
        "model": "text-embedding-ada-002",
        "encoding_format": "float"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    try:
        response = requests.post(OPENAI_API_URL, json=data, headers=headers)
        response.raise_for_status()
        embeddings = response.json()['data'][0]['embedding']
        return embeddings
    except requests.exceptions.RequestException as e:
        if attempt < 3:
            print(f"Error: {e}")
            print(f"Retrying attempt {attempt + 1}...")
            return get_embeddings_openai(text, attempt + 1)
        else:
            print(f"Error: {e}")
            return None


