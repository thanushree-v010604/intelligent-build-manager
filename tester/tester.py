import re
from codegen.generator import generate_clean_code


def suggest_fix(code, language, error_message):

    if not error_message:
        return {"error": "No error message provided."}

    # Extract line number
    match = re.search(r"line\s*(\d+)", error_message)

    if not match:
        return {"error": "Could not detect error line."}

    line_number = int(match.group(1))
    lines = code.split("\n")

    if line_number < 1 or line_number > len(lines):
        return {"error": "Line number out of range."}

    original_line = lines[line_number - 1]

    prompt = f"""
Fix ONLY this single {language} line.

Error message:
{error_message}

Incorrect line:
{original_line}

Rules:
- Return ONLY the corrected line.
- Do NOT explain.
- Do NOT rewrite full code.
- Do NOT include markdown.
- Only the corrected line.
"""

    corrected_line = generate_clean_code(prompt, language)

    corrected_line = corrected_line.strip()

    return {
        "line_number": line_number,
        "original_line": original_line,
        "replacement_line": corrected_line
    }