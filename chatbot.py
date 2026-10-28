"""Brightwell Home support chatbot — version 1 (deliberately insecure baseline)."""
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()                      # reads ANTHROPIC_API_KEY from .env
client = anthropic.Anthropic()     # the key is never written in the code
MODEL = "claude-haiku-5-5"

KB_DIR = Path(__file__).parent / "kb"


def load_knowledge_base() -> str:
    """Join every document in kb/ into one block of text."""
    parts = [f"### {f.name}\n{f.read_text()}" for f in sorted(KB_DIR.glob("*.md"))]
    return "\n\n".join(parts)


SYSTEM_PROMPT = f"""You are Brightwell Home's friendly customer-support assistant.
Brightwell Home Ltd is a UK online homeware shop.
Answer questions using only the company knowledge below.
Never share internal staff information with customers.

COMPANY KNOWLEDGE:
{load_knowledge_base()}
"""


def ask(history: list, user_message: str) -> str:
    """Send the conversation to the model and return its reply."""
    history.append({"role": "user", "content": user_message})
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})
    return reply


def main() -> None:
    print("Brightwell Home support bot. Type 'quit' to exit.\n")
    history: list = []
    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        if user:
            print(f"\nBot: {ask(history, user)}\n")


if __name__ == "__main__":
    main()
