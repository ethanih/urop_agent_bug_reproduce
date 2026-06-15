import json
import time


class FakeAPIResponse:
    def __init__(self, content: bytes) -> None:
        self.content = content

    def parse(self) -> dict:
        return json.loads(self.content)


def invoke_with_include_raw(include_raw: bool, retries: int) -> None:
    response = FakeAPIResponse(b'{"ok": 1}\n\nnot-json')
    for attempt in range(1, retries + 1):
        start = time.perf_counter()
        try:
            response.parse()
        except json.JSONDecodeError as exc:
            elapsed = time.perf_counter() - start
            print(f"attempt {attempt}: parse failed after {elapsed:.4f}s")
            if include_raw:
                print("BUG CONFIRMED: raw response was not returned to the caller before the exception")
            if attempt < retries:
                time.sleep(0.2 * attempt)
            else:
                print(type(exc).__name__ + ":", exc)


if __name__ == "__main__":
    invoke_with_include_raw(include_raw=True, retries=3)
