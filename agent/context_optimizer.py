
from agent.repository import rank_files


def build_context(workdir, task, test_output, max_files=5):
    """Select relevant source files and build compact context."""

    selected = rank_files(
        workdir=workdir,
        task=task,
        test_output=test_output,
        max_files=max_files
    )

    sections = []

    for item in selected:
        section = (
            f"FILE: {item['path']}\n"
            f"SYMBOLS: {', '.join(item['symbols'])}\n"
            f"```python\n"
            f"{item['source']}\n"
            f"```"
        )
        sections.append(section)

    context = "\n\n".join(sections)

    return {
        "context": context,
        "selected_files": [item["path"] for item in selected],
        "files_selected": len(selected),
        "files_available": len(selected),
        "context_characters": len(context)
    }
    cat > agent/context_optimizer.py <<'PY'
from agent.repository import rank_files


def build_context(workdir, task, test_output, max_files=5):
    """Select relevant source files and build compact context."""

    selected = rank_files(
        workdir=workdir,
        task=task,
        test_output=test_output,
        max_files=max_files
    )

    sections = []

    for item in selected:
        section = (
            f"FILE: {item['path']}\n"
            f"SYMBOLS: {', '.join(item['symbols'])}\n"
            f"```python\n"
            f"{item['source']}\n"
            f"```"
        )
        sections.append(section)

    context = "\n\n".join(sections)

    return {
        "context": context,
        "selected_files": [item["path"] for item in selected],
        "files_selected": len(selected),
        "files_available": len(selected),
        "context_characters": len(context)
    }
    PY