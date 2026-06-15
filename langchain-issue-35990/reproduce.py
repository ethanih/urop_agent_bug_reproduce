import json


def classify_tool_call(arguments: str) -> tuple[str, object, str | None]:
    try:
        args = json.loads(arguments)
        if not isinstance(args, dict):
            raise TypeError("Arguments must be a dictionary")
        return "tool_call", args, None
    except (json.JSONDecodeError, TypeError) as exc:
        return "invalid_tool_call", arguments, str(exc)


if __name__ == "__main__":
    kind, args, error = classify_tool_call('["not", "a", "dict"]')
    print("classification =", kind)
    print("args =", args)
    print("error =", error)
    if kind == "invalid_tool_call":
        print("BUG BOUNDARY REPRODUCED: non-dict args must not be treated as valid tool calls")
