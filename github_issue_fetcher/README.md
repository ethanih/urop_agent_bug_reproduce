# GitHub Issue Fetcher

Fetch the original author's GitHub issue description and save it as a Markdown file.

## Environment

This script only uses the Python standard library.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

```bash
python fetch.py https://github.com/owner/repo/issues/123
```

Write to a specific file:

```bash
python fetch.py https://github.com/owner/repo/issues/123 -o output.md
```

Write into a directory:

```bash
python fetch.py https://github.com/owner/repo/issues/123 -o issues/
```
