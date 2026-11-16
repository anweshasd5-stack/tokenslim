
import json
from pathlib import Path

from agent.llm import LLM
from agent.coding_agent import run_optimized


def main():
    task_root = Path("tasks")

    if not task_root.exists():
        raise FileNotFoundError("The tasks directory does not exist.")

    results = []

    for task_dir in sorted(task_root.iterdir()):
        if not task_dir.is_dir():
            continue

        print(f"\nRunning TokenSlim on: {task_dir.name}")

        llm = LLM()

        outcome = run_optimized(
            task_dir,
            llm,
            task_description="Fix the failing Python tests without modifying tests."
        )

        results.append(outcome)

        status = "PASS" if outcome["passed"] else "FAIL"

        print(
            f"{task_dir.name}: {status} | "
            f"Tokens: {outcome['tokens']} | "
            f"Calls: {outcome['calls']}"
        )

    Path("results").mkdir(exist_ok=True)

    Path("results/optimized.json").write_text(
        json.dumps(results, indent=2)
    )

    total_tokens = sum(item["tokens"] for item in results)
    passed = sum(item["passed"] for item in results)

    print("\nTOKENSLIM X RESULTS")
    print(f"Passed: {passed}/{len(results)}")
    print(f"Total tokens: {total_tokens}")


if __name__ == "__main__":
    main()
