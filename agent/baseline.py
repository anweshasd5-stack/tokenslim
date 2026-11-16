import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SYSTEM = (
    "You are a coding agent. You are given a Python project whose tests fail. "
    "Fix the bug. Reply with the COMPLETE fixed contents of every file you change, "
    "using exactly this format for each file:\n"
    "FILE: relative/path.py\n```python\n<entire file contents>\n```\n"
    "Do not change the tests."
)

FILE_BLOCK = re.compile(r"FILE:\s*(\S+)\s*\n```(?:python)?\n(.*?)```", re.DOTALL)


def run_tests(workdir):
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-x"],
        cwd=workdir,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, result.stdout + result.stderr


def run_baseline(task_dir, llm):
    """Naive agent: dumps every .py file into the prompt, gets whole files back."""
    task_dir = Path(task_dir)
    workdir = Path(tempfile.mkdtemp()) / task_dir.name
    shutil.copytree(task_dir, workdir)

    start_tokens = llm.total_tokens
    _, test_output = run_tests(workdir)

    files_text = ""
    for path in sorted(workdir.rglob("*.py")):
        files_text += f"FILE: {path.relative_to(workdir)}\n```python\n{path.read_text()}\n```\n\n"

    user_msg = f"{files_text}Test output:\n{test_output}\n\nFix the bug."
    reply = llm.chat(
        [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user_msg}]
    )

    for rel_path, content in FILE_BLOCK.findall(reply):
        target = workdir / rel_path
        if target.exists() and not rel_path.startswith("test_"):
            target.write_text(content)

    passed, _ = run_tests(workdir)
    shutil.rmtree(workdir.parent, ignore_errors=True)
    return {
        "task": task_dir.name,
        "passed": passed,
        "tokens": llm.total_tokens - start_tokens,
    }
