def parse_result(results: list[dict], partial: bool) -> list[object]:
    name_dict = {
        "Model1": lambda **kwargs: ("Model1", kwargs),
        "Model2": lambda **kwargs: ("Model2", kwargs),
    }
    parsed = []
    for res in results:
        parsed.append(name_dict[res["type"]](**res["args"]))
    return parsed


if __name__ == "__main__":
    results = [
        {"type": "Model1", "args": {"name": "Alice", "age": 30}},
        {"type": "Model3", "args": {"value": 3.14}},
    ]
    try:
        parse_result(results, partial=True)
    except KeyError as exc:
        print("BUG CONFIRMED:", repr(exc))
