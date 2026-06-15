import json
import os
from dataclasses import dataclass


@dataclass
class Joke:
    setup: str
    punchline: str
    rating: int | None = None


class OutputParserException(Exception):
    pass


def parse_structured_output(text: str) -> Joke:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise OutputParserException("Invalid json output") from exc
    return Joke(**data)


def local_approximation() -> None:
    bad_model_output = "I will think step by step before answering."
    try:
        parse_structured_output(bad_model_output)
    except OutputParserException as exc:
        print("BUG CONFIRMED: structured output parse failed")
        print(type(exc).__name__ + ":", exc)
        print("Cause:", type(exc.__cause__).__name__, exc.__cause__)


def real_ollama_repro() -> None:
    from langchain_ollama import ChatOllama
    from pydantic import BaseModel, Field

    class JokeModel(BaseModel):
        setup: str = Field(description="The setup of the joke")
        punchline: str = Field(description="The punchline to the joke")
        rating: int | None = Field(default=None, description="How funny it is")

    llm = ChatOllama(model="gpt-oss:20b", reasoning=True)
    structured_llm = llm.with_structured_output(JokeModel, method="json_schema")
    print(structured_llm.invoke("Tell me a joke about cats"))


if __name__ == "__main__":
    if os.getenv("USE_REAL_OLLAMA") == "1":
        real_ollama_repro()
    else:
        local_approximation()
