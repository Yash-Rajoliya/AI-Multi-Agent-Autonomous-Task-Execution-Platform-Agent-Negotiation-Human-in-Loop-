import subprocess
from datetime import datetime


class ChangelogGenerator:
    def __init__(self):
        self.output_file = "CHANGELOG.md"

    def get_git_logs(self) -> str:
        return subprocess.check_output(
            ["git", "log", "--pretty=format:%h - %s (%an)", "--no-merges"]
        ).decode()

    def generate(self):
        logs = self.get_git_logs()
        now = datetime.utcnow().strftime("%Y-%m-%d")

        content = f"# Changelog\n\n## {now}\n\n"
        for line in logs.split("\n"):
            content += f"- {line}\n"

        with open(self.output_file, "w") as f:
            f.write(content)

        print("Changelog generated.")


if __name__ == "__main__":
    ChangelogGenerator().generate()