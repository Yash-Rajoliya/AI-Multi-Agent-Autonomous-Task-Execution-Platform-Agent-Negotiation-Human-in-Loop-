import subprocess
from datetime import datetime


class VersionManager:
    def __init__(self):
        self.base_version = "0.1.0"

    def get_git_commit_hash(self) -> str:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()

    def generate_version(self) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M")
        commit = self.get_git_commit_hash()
        return f"{self.base_version}-{timestamp}-{commit}"

    def tag_release(self, version: str):
        subprocess.run(["git", "tag", version])
        subprocess.run(["git", "push", "origin", version])


if __name__ == "__main__":
    manager = VersionManager()
    version = manager.generate_version()
    print(f"Generated version: {version}")
    manager.tag_release(version)