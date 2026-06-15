from dataclasses import dataclass, field


@dataclass
class AIMessage:
    tool_calls: list[dict] = field(default_factory=list)
    invalid_tool_calls: list[dict] = field(default_factory=list)


def current_route(message: AIMessage) -> str:
    if len(message.tool_calls) == 0:
        return "end"
    return "tools"


def expected_route(message: AIMessage) -> str:
    if len(message.tool_calls) == 0 and len(message.invalid_tool_calls) == 0:
        return "end"
    return "tools_or_error_feedback"


if __name__ == "__main__":
    message = AIMessage(
        tool_calls=[],
        invalid_tool_calls=[
            {
                "id": "call-123",
                "name": "write_file",
                "args": '{"file_path": "test.txt", "content": "Hello World"]',
                "error": "Expecting ',' delimiter",
            }
        ],
    )
    print("current_route =", current_route(message))
    print("expected_route =", expected_route(message))
    if current_route(message) == "end":
        print("BUG CONFIRMED: invalid_tool_calls are ignored and the agent exits early")
