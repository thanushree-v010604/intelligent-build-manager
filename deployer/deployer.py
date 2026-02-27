import tempfile
import subprocess
import random
import sys
import re


FORBIDDEN_IMPORTS = [
    "flask_sqlalchemy",
    "flask_session",
    "flask_login",
    "flask_wtf",
    "flask_migrate",
]


def clean_code(code):
    lines = code.split("\n")
    cleaned = []

    for line in lines:
        if any(pkg in line for pkg in FORBIDDEN_IMPORTS):
            continue
        cleaned.append(line)

    return "\n".join(cleaned)


def deploy_project(code, language):
    try:
        port = random.randint(5001, 5999)

        if language.lower() == "python":

            # 🔥 Remove forbidden imports
            code = clean_code(code)

            # 🔥 Remove existing __main__ block
            code = re.sub(
                r'if\s+__name__\s*==\s*["\']__main__["\']\s*:\s*(?:\n\s+.*)*',
                '',
                code
            )

            # 🔥 Replace render_template
            if "render_template(" in code:
                code = code.replace(
                    "render_template(",
                    'render_template_string("<h1>Templates not supported. Inline HTML required.</h1>") #'
                )

            # 🔥 Append safe run block
            code += f"""

if __name__ == "__main__":
    app.run(host="127.0.0.1", port={port}, debug=False)
"""

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
            temp_file.write(code.encode())
            temp_file.close()

            subprocess.Popen([sys.executable, temp_file.name])

            return {{
                "status": "success",
                "live_url": f"http://127.0.0.1:{port}"
            }}

        elif language.lower() == "html":
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            temp_file.write(code.encode())
            temp_file.close()

            return {{
                "status": "success",
                "live_url": temp_file.name
            }}

        else:
            return {{
                "status": "failure",
                "live_url": "Deployment supported only for Python (Flask) and HTML"
            }}

    except Exception as e:
        return {{
            "status": "failure",
            "live_url": str(e)
        }}