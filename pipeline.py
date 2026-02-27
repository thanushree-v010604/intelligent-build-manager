from codegen.generator import generate_clean_code
from builder.builder import build_code
from tester.tester import suggest_fix
from deployer.deployer import deploy_project


def run_pipeline(stage, prompt=None, code=None, language=None):

    if stage == "generate":
        generated = generate_clean_code(prompt, language)
        return {
            "status": "success",
            "code": generated
        }

    elif stage == "build":
        success, message = build_code(code, language)

        return {
            "status": "success" if success else "failure",
            "message": message,
            "code": code
        }

    elif stage == "suggest":
        suggestion = suggest_fix(code, language, prompt)
        return {
            "status": "success",
            "suggestion": suggestion
        }
    elif stage == "explain":
        return {
        "explanation": f"""
This code is written in {language}.

Overview:
This program defines application behavior and execution flow.

What It Does:
- Imports required modules.
- Configures the application setup.
- Defines main logic or routes.
- Executes the program.

Beginner Explanation:
Think of this code as a set of instructions telling the computer
what to do step-by-step.
"""
    }
    