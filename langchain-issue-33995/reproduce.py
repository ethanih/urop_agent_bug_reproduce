import json
import os


class BadRequestError(Exception):
    pass


def simulate_provider(required_tool_call: bool, model_output: str, called_tool: bool) -> None:
    json.loads(model_output)
    if required_tool_call and not called_tool:
        raise BadRequestError("Tool choice is required, but model did not call a tool")


def local_approximation() -> None:
    try:
        simulate_provider(
            required_tool_call=True,
            model_output='{"main_artists":["DIRE STRAITS"],"title":"walk of life"}',
            called_tool=False,
        )
    except BadRequestError as exc:
        print("BUG CONFIRMED:", exc)


def real_groq_repro() -> None:
    from pydantic import BaseModel, Field
    from langchain_groq import ChatGroq
    from langchain.messages import HumanMessage, SystemMessage

    class Track(BaseModel):
        main_artists: list[str] = Field(description="Names of all unique Main-Artists for this track.")
        title: str = Field(description="Track title as released.")

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=os.environ["GROQ_API_KEY"],
    ).with_structured_output(Track)

    message = [
        SystemMessage("You are a parser for Music-Records respond only with the given json format. You do not need any Tools!"),
        HumanMessage("RECORD_TITLE: walk of life; MAIN_ARTIST: DIRE STRAITS;"),
    ]
    print(llm.invoke(message))


if __name__ == "__main__":
    if os.getenv("USE_REAL_GROQ") == "1":
        real_groq_repro()
    else:
        local_approximation()
