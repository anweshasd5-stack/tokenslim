import json
from pathlib import Path

from agent.baseline import run_baseline
from agent.llm import LLM

results = []
for task_dir in sorted(Path("tasks").iterdir()):
    if not task_dir.is_dir():
        continue
    llm = LLM()
    outcome = run_baseline(task_dir, llm)
    results.append(outcome)
    status = "PASS" if outcome["passed"] else "FAIL"
    print(f"{outcome['task']}: {status}  tokens={outcome['tokens']}")

Path("results").mkdir(exist_ok=True)
Path("results/baseline.json").write_text(json.dumps(results, indent=2))
total = sum(r["tokens"] for r in results)
passed = sum(r["passed"] for r in results)
print(f"\nBaseline: {passed}/{len(results)} passed, {total} total tokens")
