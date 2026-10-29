"""Checks that a workstation is ready for the Glosix Agentic AI internship.

Run with:  uv run setup-check
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable

MIN_PYTHON: tuple[int, int] = (3, 12)


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str
    required: bool = True


Runner = Callable[[list[str]], str | None]


def run_command(cmd: list[str]) -> str | None:
    """Run a command and return its trimmed output, or None if it fails."""
    if shutil.which(cmd[0]) is None:
        return None
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return (out.stdout or out.stderr).strip()


def check_python(version: tuple[int, int] = sys.version_info[:2]) -> CheckResult:
    ok = version >= MIN_PYTHON
    found = f"{version[0]}.{version[1]}"
    need = f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}+"
    return CheckResult("Python", ok, f"found {found}, need {need}")


def check_tool(name: str, cmd: list[str], run: Runner, required: bool = True) -> CheckResult:
    output = run(cmd)
    if output is None:
        return CheckResult(name, False, "not found", required)
    return CheckResult(name, True, output.splitlines()[0], required)


def check_git_identity(run: Runner) -> CheckResult:
    user = run(["git", "config", "--global", "user.name"])
    email = run(["git", "config", "--global", "user.email"])
    if user and email:
        return CheckResult("Git identity", True, f"{user} <{email}>")
    return CheckResult("Git identity", False, "run: git config --global user.name / user.email")


def check_github_auth(run: Runner) -> CheckResult:
    status = run(["gh", "auth", "status"])
    if status is not None:
        return CheckResult("GitHub login (gh)", True, "logged in", required=False)
    return CheckResult("GitHub login (gh)", False, "optional: run gh auth login", required=False)


def run_all(run: Runner = run_command) -> list[CheckResult]:
    return [
        check_python(),
        check_tool("Git", ["git", "--version"], run),
        check_tool("uv", ["uv", "--version"], run),
        check_git_identity(run),
        check_tool("Docker", ["docker", "--version"], run, required=False),
        check_tool("Ollama", ["ollama", "--version"], run, required=False),
        check_tool("VS Code", ["code", "--version"], run, required=False),
        check_github_auth(run),
    ]


def format_report(results: list[CheckResult]) -> str:
    lines = []
    for r in results:
        mark = "OK  " if r.ok else ("FAIL" if r.required else "TODO")
        lines.append(f"[{mark}] {r.name:<18} {r.detail}")
    return "\n".join(lines)


def is_ready(results: list[CheckResult]) -> bool:
    return all(r.ok for r in results if r.required)


def main() -> int:
    results = run_all()
    print(format_report(results))
    if is_ready(results):
        print("\nReady for Day 1. Optional TODO items are needed later in the program.")
        return 0
    print("\nFix the FAIL items above, then run this again.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
