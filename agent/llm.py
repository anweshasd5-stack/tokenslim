 
import os
import time

from dotenv import load_dotenv
from openai import OpenAI, APIError

load_dotenv()


class LLM:
    """Thin wrapper around an OpenAI-compatible API that counts every token."""

    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ["LLM_API_KEY"],
            base_url=os.environ.get("LLM_BASE_URL") or None,
            timeout=30.0,
            max_retries=0,
        )
        self.model = os.environ["LLM_MODEL"]
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.calls = 0

    
    def chat(self, messages):
        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0,
                    timeout=60.0
                )

                usage = response.usage
                self.calls += 1

                if usage:
                    self.prompt_tokens += usage.prompt_tokens or 0
                    self.completion_tokens += usage.completion_tokens or 0

                return response.choices[0].message.content or ""

            except APIError as e:
                print(f"API attempt {attempt + 1}/3 failed: {e}")

                if attempt == 2:
                    raise

                wait_seconds = 2 ** attempt
                print(f"Retrying in {wait_seconds} seconds...")
                time.sleep(wait_seconds)
