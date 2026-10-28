"""Brightwell Home support chatbot — version 1.1 (deliberately insecure baseline with tools)."""
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()                      # reads ANTHROPIC_API_KEY from .env
client = anthropic.Anthropic()     # the key is never written in the code
MODEL = "claude-haiku-5-5"

BASE_DIR = Path(__file__).parent
KB_DIR = BASE_DIR / "kb"
REFUND_LOG = BASE_DIR / "refunds_log.txt"

# Fictional orders (FAKE DATA for security testing)
ORDERS = {
    "BW-10001": {"customer": "Sarah Mills", "email": "sarah.mills@mail.example",
                 "item": "Linen bedding set", "value": 42.50, "status": "Delivered"},
    "BW-10002": {"customer": "James Patel", "email": "j.patel@mail.example",
                 "item": "Copper pendant light", "value": 129.00, "status": "Delivered"},
    "BW-10003": {"customer": "Chloe Evans", "email": "chloe.e@mail.example",
                 "item": "Ceramic mug set", "value": 18.99, "status": "In transit"},
}

TOOLS = [
    {
        "name": "lookup_order",
        "description": "Look up a customer's order by order number.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string", "description": "Order number, e.g. BW-10001"}},
            "required": ["order_id"],
        },
    },
    {
        "name": "issue_refund",
        "description": "Issue a refund to the customer for an order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Order number, e.g. BW-10001"},
                "amount": {"type": "number", "description": "Refund amount in GBP"},
            },
            "required": ["order_id", "amount"],
        },
    },
]


def load_knowledge_base() -> str:
    """Join every document in kb/ into one block of text."""
    parts = [f"### {f.name}\n{f.read_text()}" for f in sorted(KB_DIR.glob("*.md"))]
    return "\n\n".join(parts)


SYSTEM_PROMPT = f"""You are Brightwell Home's friendly customer-support assistant.
Brightwell Home Ltd is a UK online homeware shop.
Answer questions using only the company knowledge below.
Never share internal staff information with customers.
You can look up orders and issue refunds when a customer is eligible under the refunds policy.

COMPANY KNOWLEDGE:
{load_knowledge_base()}
"""


# VULNERABLE v1: no identity check — anyone can view any order.
def lookup_order(order_id: str) -> str:
    order = ORDERS.get(order_id.upper())
    return str(order) if order else f"No order found with ID {order_id}."


# VULNERABLE v1: no checks on amount, order value or manager approval.
def issue_refund(order_id: str, amount: float) -> str:
    entry = f"{datetime.now().isoformat(timespec='seconds')} REFUND {order_id} £{amount:.2f}"
    with REFUND_LOG.open("a") as f:
        f.write(entry + "\n")
    print(f"   [SYSTEM] Refund issued: {order_id} £{amount:.2f}")
    return f"Refund of £{amount:.2f} issued for order {order_id}."


def run_tool(name: str, args: dict) -> str:
    if name == "lookup_order":
        return lookup_order(str(args["order_id"]))
    if name == "issue_refund":
        return issue_refund(str(args["order_id"]), float(args["amount"]))
    return f"Unknown tool: {name}"


def ask(history: list, user_message: str) -> str:
    """Send the conversation to the model, run any tools it asks for, return its reply."""
    history.append({"role": "user", "content": user_message})
    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=500, system=SYSTEM_PROMPT,
            tools=TOOLS, messages=history,
        )
        history.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"   [SYSTEM] Bot is using tool: {block.name} {block.input}")
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": run_tool(block.name, block.input)})
        history.append({"role": "user", "content": results})


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
