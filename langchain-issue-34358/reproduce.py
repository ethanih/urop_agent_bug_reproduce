def process_selection_response(response: dict) -> list[str]:
    selected = []
    for tool_name in response["tools"]:
        selected.append(tool_name)
    return selected


if __name__ == "__main__":
    malformed_response = {"reason": "No tools needed"}
    try:
        process_selection_response(malformed_response)
    except KeyError as exc:
        print("BUG CONFIRMED:", repr(exc))
