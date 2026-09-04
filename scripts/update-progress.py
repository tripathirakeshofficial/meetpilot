#!/usr/bin/env python3
# noqa: EXE001
import re
import subprocess
from datetime import datetime, timezone

START_MARKER = "<!-- AUTO_PROGRESS_START -->"
END_MARKER = "<!-- AUTO_PROGRESS_END -->"


def run(command):
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip()


def get_commit_message():
    return run("git log -1 --pretty=%s")


def get_commit_hash():
    return run("git log -1 --pretty=%h")


def get_changed_files():
    output = run("git diff-tree --no-commit-id --name-status -r HEAD")

    changes = []

    for line in output.splitlines():
        parts = line.split("\t", 1)

        if len(parts) == 2:
            status, path = parts

            if path == "README.md":
                continue

            changes.append((status, path))

    return changes


def classify_changes(changes):
    categories = {
        "frontend": [],
        "backend": [],
        "database": [],
        "configuration": [],
        "documentation": [],
        "testing": [],
        "automation": [],
        "other": [],
    }

    for status, path in changes:
        lower = path.lower()

        if lower.startswith(("app/", "components/", "pages/")) or lower.endswith(
            (".tsx", ".jsx", ".css")
        ):
            categories["frontend"].append(path)

        elif lower.startswith(("api/", "server/", "backend/")):
            categories["backend"].append(path)

        elif (
            "prisma" in lower
            or "migration" in lower
            or "database" in lower
            or lower.endswith((".sql",))
        ):
            categories["database"].append(path)

        elif (
            lower.startswith((".github/", ".devcontainer/"))
            or "docker" in lower
            or lower.endswith((".yml", ".yaml"))
        ):
            categories["automation"].append(path)

        elif (
            lower.startswith("test")
            or "__tests__" in lower
            or ".test." in lower
            or ".spec." in lower
        ):
            categories["testing"].append(path)

        elif lower.endswith((".md", ".mdx")):
            categories["documentation"].append(path)

        elif (
            lower.endswith((".json", ".toml", ".ini"))
            or lower.startswith(".env")
            or lower in ("package.json", "tsconfig.json")
        ):
            categories["configuration"].append(path)

        else:
            categories["other"].append(path)

    return categories


def build_progress(changes):
    commit_message = get_commit_message()

    progress = []

    if commit_message:
        progress.append(f"Completed: {commit_message}.")

    if not progress:
        progress.append(
            f"Implemented changes associated with commit `{commit_message}`."
        )

    return progress


def update_readme(progress):
    readme_path = "README.md"

    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )

    latest_progress = "\n".join(f"- {item}" for item in progress)

    replacement = f"""{START_MARKER}

**Current Phase:** Active Development

### Latest Progress
{latest_progress}

### Next Steps
Continue implementing and validating the next major MeetPilot feature.

_Last updated: {datetime.now(timezone.utc).date().isoformat()}_

{END_MARKER}"""

    updated_content, count = pattern.subn(replacement, content, count=1)

    if count == 0:
        raise RuntimeError("README.md does not contain the AUTO_PROGRESS markers.")

    if updated_content != content:
        with open(readme_path, "w", encoding="utf-8") as file:
            file.write(updated_content)

        print("README.md progress section updated.")
    else:
        print("README.md progress section already up to date.")


def main():
    changes = get_changed_files()

    if not changes:
        print("No changed files detected.")
        return

    progress = build_progress(changes)

    print("\nGenerated progress:")
    for item in progress:
        print(f"- {item}")

    update_readme(progress)


if __name__ == "__main__":
    main()
