#!/usr/bin/env python3
"""Minimal reproduction for openai/codex issue #666."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory


def generate_files() -> dict[str, str]:
    return {
        "App.vue": "<template><h1>Hello from generated app</h1></template>\n",
        "main.js": "console.log('boot app')\n",
    }


def create_files_buggy(target_dir: Path, generated_files: dict[str, str]) -> None:
    for name in generated_files:
        # Bug reproduction: the file is created, but the generated content is dropped.
        (target_dir / name).write_text("")


def main() -> int:
    with TemporaryDirectory() as tmpdir:
        target_dir = Path(tmpdir)
        generated = generate_files()
        create_files_buggy(target_dir, generated)

        for name, expected in generated.items():
            actual = (target_dir / name).read_text()
            print(f"Generated content for {name}:")
            print(expected, end="")
            print()
            print(f"Actual file content on disk for {name}:")
            print(repr(actual))
            print()
            assert actual == ""

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
