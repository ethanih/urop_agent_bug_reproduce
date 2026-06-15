import json


def parse_message_content(content: list[dict]) -> dict:
    raw_text = "".join(part["text"] for part in content if part.get("type") == "text")
    return json.loads(raw_text)


if __name__ == "__main__":
    content = [
        {"type": "text", "phase": "commentary", "text": '{"some_field": "some text"}'},
        {"type": "text", "phase": "final_answer", "text": '{"some_field": "some other text"}'},
    ]
    try:
        parse_message_content(content)
    except json.JSONDecodeError as exc:
        print("BUG CONFIRMED:", type(exc).__name__, exc)
