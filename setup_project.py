cat > check_llm.py <<'EOF'
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key = os.environ.get("LLM_API_KEY", "")
base = os.environ.get("LLM_BASE_URL") or None
print("key set:", bool(key) and key != "your_key_here", "| key length:", len(key))
print("model in .env:", os.environ.get("LLM_MODEL"))

client = OpenAI(api_key=key, base_url=base)

for model in ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-flash-latest"]:
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hi"}],
        )
        print("WORKS:", model)
    except Exception as e:
        body = getattr(e, "body", None) or str(e)
        print("FAILED:", model, "->", str(body)[:300])
EOF