
import ast
import re
from pathlib import Path


def extract_identifiers(text):
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", text.lower()))


def inspect_python_file(path):
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        symbols = set()

        for node in ast.walk(tree):
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                symbols.add(node.name.lower())

        return source, symbols

    except (OSError, SyntaxError, UnicodeDecodeError):
        return "", set()


def rank_files(workdir, task, test_output, max_files=5):
    workdir = Path(workdir)

    query = extract_identifiers(task + " " + test_output)
    ranked = []
    files_available = 0

    for path in sorted(workdir.rglob("*.py")):
        relative = path.relative_to(workdir)

        if (
            "__pycache__" in relative.parts
            or any(part.startswith(".") for part in relative.parts)
            or path.name.startswith("test_")
            or path.name.endswith("_test.py")
            or "tests" in relative.parts
        ):
            continue

        source, symbols = inspect_python_file(path)

        if not source:
            continue

        files_available += 1

        filename_terms = extract_identifiers(path.stem)
        content_terms = extract_identifiers(source)

        score = (
            len(query & filename_terms) * 5
            + len(query & symbols) * 4
            + len(query & content_terms)
        )

        ranked.append({
            "path": relative.as_posix(),
            "source": source,
            "score": score,
            "symbols": sorted(symbols)
        })

    ranked.sort(
        key=lambda item: (-item["score"], item["path"])
    )

    selected = [
        item for item in ranked if item["score"] > 0
    ][:max_files]

    if not selected:
        selected = ranked[:min(3, max_files)]

    return selected
