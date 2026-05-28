import subprocess
import tempfile
import os


class CodeRunner:
    def __init__(self, timeout=5):
        self.timeout = timeout

    def run_python(self, code: str):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(code.encode())
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                ["python", tmp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

        finally:
            os.remove(tmp_path)