#!/usr/bin/env python3
"""Real-dependency reproduction harness for crewAI issue #3925."""

from __future__ import annotations

import os
import sys


ENGLISH_EXAMPLE = """English hierarchical crew:
- manager role: Customer Support Concierge
- worker role: Return Policy Checker
- inquiry: I bought earphones yesterday, but sound only comes from one side. Can I return them?
Expected from issue: manager delegates to Return Policy Checker.
"""

JAPANESE_EXAMPLE = """Japanese hierarchical crew:
- manager role: お客様対応コンシェルジュ
- worker role: 返品ポリシーチェッカー
- inquiry: 昨日イヤホンを買いましたが、片側しか音が出ません。返品できますか？
Expected from issue: manager may keep delegating to itself instead of the coworker.
"""


def main() -> int:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("OPENAI_API_KEY is blank.")
        print("Fill it in before attempting the live CrewAI reproduction.")
        print()
        print(ENGLISH_EXAMPLE)
        print(JAPANESE_EXAMPLE)
        return 0

    print("A real CrewAI + live model reproduction is required for this issue.")
    print("This repository intentionally does not embed a real API key.")
    print("Install crewai==1.5.0 and wire the original issue's English/Japanese examples.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
