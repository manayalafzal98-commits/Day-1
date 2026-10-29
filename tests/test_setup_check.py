from day1_starter.setup_check import (
    CheckResult,
    check_git_identity,
    check_python,
    check_tool,
    format_report,
    is_ready,
    run_all,
)


def fake_runner(answers: dict[str, str | None]):
    def run(cmd: list[str]) -> str | None:
        return answers.get(" ".join(cmd))
    return run


def test_python_new_enough():
    assert check_python((3, 12)).ok
    assert check_python((3, 13)).ok


def test_python_too_old():
    result = check_python((3, 11))
    assert not result.ok
    assert "3.11" in result.detail


def test_tool_found_uses_first_line():
    run = fake_runner({"uv --version": "uv 0.5.0\nextra"})
    result = check_tool("uv", ["uv", "--version"], run)
    assert result.ok and result.detail == "uv 0.5.0"


def test_tool_missing():
    result = check_tool("uv", ["uv", "--version"], fake_runner({}))
    assert not result.ok and result.detail == "not found"


def test_git_identity_set():
    run = fake_runner({
        "git config --global user.name": "Yahya Khan",
        "git config --global user.email": "me@example.com",
    })
    assert check_git_identity(run).ok


def test_git_identity_missing_email():
    run = fake_runner({"git config --global user.name": "Yahya Khan"})
    assert not check_git_identity(run).ok


def test_optional_failures_do_not_block():
    results = [
        CheckResult("Git", True, "ok"),
        CheckResult("Docker", False, "not found", required=False),
    ]
    assert is_ready(results)
    assert "[TODO] Docker" in format_report(results)


def test_required_failure_blocks():
    results = [CheckResult("Git", False, "not found")]
    assert not is_ready(results)
    assert "[FAIL] Git" in format_report(results)


def test_run_all_covers_every_check():
    names = [r.name for r in run_all(fake_runner({}))]
    assert names[:4] == ["Python", "Git", "uv", "Git identity"]
    assert len(names) == 8
