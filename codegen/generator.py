import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_clean_code(prompt, language):
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found in .env"

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = f"""
Generate a complete runnable web application in {language}.

Strict Rules:
- Must create a working website.
- Must include server setup.
- Must include routes.
- Must render HTML.
- Must run immediately when executed.
- Use only basic Flask.
- Do NOT use flask_sqlalchemy.
- Do NOT use external Flask extensions.
- Do NOT use render_template().
- Do NOT use templates folder.
- Use render_template_string() only.
- Everything must be inside one single file.
- No comments.
- No markdown.
- No explanations.
- Only pure executable code.

If Python → use basic Flask only.
If JavaScript → use Express.
If HTML → return full standalone HTML page.
"""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            return f"Groq API Error: {response.text}"

        data = response.json()

        code = data["choices"][0]["message"]["content"].strip()

        # Remove markdown wrappers if model adds them
        code = code.replace("```python", "")
        code = code.replace("```javascript", "")
        code = code.replace("```html", "")
        code = code.replace("```", "")

        return code.strip()

    except Exception as e:
        return f"Server Error: {str(e)}"
        