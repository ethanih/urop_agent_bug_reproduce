class StructuredOutputValidationError(Exception):
    pass


def handle_structured_output(tool_calls: list[dict], handle_errors: bool) -> dict:
    if tool_calls:
        return {"structured_response": tool_calls[0]["args"]}
    if handle_errors:
        return {"messages": ["retry requested"]}
    return {"messages": ["model replied, but no tool call was made"]}


if __name__ == "__main__":
    response = handle_structured_output(tool_calls=[], handle_errors=False)
    print(response)
    if "structured_response" not in response:
        print("BUG CONFIRMED: no exception and no structured_response for missing tool call")
