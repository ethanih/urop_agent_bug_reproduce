"""Minimal reproduction for langchain-ai/langchain#34358.

This script models the reported failure mechanism only:
direct iteration over response["tools"] without schema validation.
"""


def process_selection_response(response: dict) -> list[str]:
    selected = []
    for tool_name in response["tools"]:
        selected.append(tool_name)
    return selected


def main() -> None:
    malformed_response = {"reason": "No tools needed"}
    print("Running reproduction with malformed selector response:")
    print(malformed_response)
    process_selection_response(malformed_response)


if __name__ == "__main__":
    main()
