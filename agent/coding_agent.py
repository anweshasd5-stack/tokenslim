
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from agent.baseline import run_tests
from agent.context_optimizer import build_context


SYSTEM_PROMPT = """
You are TokenSlim X, an expert Python coding agent.

Your objective is to fix the reported bug using the
smallest possible code change.

RULES:
1. Do not modify test files.
2. Preserve existing APIs and behavior.
3. Avoid unnecessary code changes.
4. Return ONLY a valid unified diff.
5. Use paths relative to the project root.
6. Include --- a/path and +++ b/path headers.
7. Do not include markdown fences or explanations.
8. If no safe fix is possible, return NO_PATCH.
"""


def validate_patch(patch, workdir):
    if not patch.strip() or patch.strip() == "NO_PATCH":
        return False

    workdir = Path(workdir).resolve()
    paths = []

    for line in patch.splitlines():
        if line.startswith(("--- ", "+++ ")):
            raw = line[4:].split("\t")[0].strip()

            if raw == "/dev/null":
                return False

            if raw.startswith(("a/", "b/")):
                raw = raw[2:]

            candidate = Path(raw)

            if candidate.is_absolute() or ".." in candidate.parts:
                return False

            if (
                candidate.name.startswith("test_")
                or candidate.name.endswith("_test.py")
                or "tests" in candidate.parts
            ):
                return False

            target = (workdir / candidate).resolve()

            if not target.is_relative_to(workdir):
                return False

            if not target.is_file():
                return False

            paths.append(target)

    return bool(paths) and len(paths) % 2 == 0


def apply_patch(patch, workdir):
    if not validate_patch(patch, workdir):
        return False

    patch_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".patch",
            encoding="utf-8",
            delete=False
        ) as file:
            file.write(patch)
            patch_path = file.name

        check = subprocess.run(
            ["git", "apply", "--check", "--whitespace=error", patch_path],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=20
        )

        if check.returncode != 0:
            return False

        result = subprocess.run(
            ["git", "apply", "--whitespace=error", patch_path],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=20
        )

        return result.returncode == 0

    except (OSError, subprocess.TimeoutExpired):
        return False

    finally:
        if patch_path:
            Path(patch_path).unlink(missing_ok=True)


def run_optimized(task_dir, llm, task_description=None):
    task_dir = Path(task_dir).resolve()

    parent = Path(tempfile.mkdtemp(prefix="tokenslim_"))
    workdir = parent / task_dir.name

    start_tokens = llm.total_tokens
    start_calls = llm.calls
    start_time = time.perf_counter()

    try:
        shutil.copytree(task_dir, workdir)

        initial_pass, test_output = run_tests(workdir)

        if initial_pass:
            return {
                "task": task_dir.name,
                "passed": True,
                "tokens": 0,
                "calls": 0,
                "patch_applied": False
            }

        description = task_description or (
            "Fix the failing Python project tests."
        )

        optimized = build_context(
            workdir,
            description,
            test_output
        )

        user_message = (
            f"TASK:\n{description}\n\n"
            f"FAILING TESTS:\n{test_output}\n\n"
            f"RELEVANT SOURCE CODE:\n{optimized['context']}\n\n"
            "Return the smallest valid unified diff."
        )

        reply = llm.chat([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ])

        applied = apply_patch(reply, workdir)

        if applied:
            passed, verification = run_tests(workdir)
        else:
            passed = False
            verification = "Patch rejected or could not be applied."

        return {
            "task": task_dir.name,
            "passed": passed,
            "tokens": llm.total_tokens - start_tokens,
            "calls": llm.calls - start_calls,
            "latency_seconds": round(
                time.perf_counter() - start_time, 3
            ),
            "files_selected": optimized["files_selected"],
            "context_characters": optimized["context_characters"],
            "patch_applied": applied,
            "verification_output": verification[:2000]
        }

    finally:
        shutil.rmtree(parent, ignore_errors=True)
