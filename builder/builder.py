import tempfile
import subprocess


def build_code(code, language):

    try:

        # ---------- PYTHON ----------
        if language.lower() == "python":
            compile(code, "<string>", "exec")
            return True, "Build successful"

        # ---------- JAVASCRIPT ----------
        elif language.lower() == "javascript":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as f:
                f.write(code.encode())
                filename = f.name

            result = subprocess.run(
                ["node", "--check", filename],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False, result.stderr

            return True, "Build successful"

        # ---------- C ----------
        elif language.lower() == "c":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as f:
                f.write(code.encode())
                filename = f.name

            result = subprocess.run(
                ["gcc", filename],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False, result.stderr

            return True, "Build successful"

        # ---------- C++ ----------
        elif language.lower() == "cpp":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as f:
                f.write(code.encode())
                filename = f.name

            result = subprocess.run(
                ["g++", filename],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False, result.stderr

            return True, "Build successful"

        # ---------- JAVA ----------
        elif language.lower() == "java":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as f:
                f.write(code.encode())
                filename = f.name

            result = subprocess.run(
                ["javac", filename],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False, result.stderr

            return True, "Build successful"

        else:
            return False, "Unsupported language"

    except Exception as e:
        return False, str(e)