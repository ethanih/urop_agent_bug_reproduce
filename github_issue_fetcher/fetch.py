#!/usr/bin/env python3
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


ISSUE_URL_RE = re.compile(
    r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/issues/(?P<number>\d+)(?:[/?#].*)?$"
)


def parse_issue_url(issue_url: str) -> tuple[str, str, str]:
    match = ISSUE_URL_RE.match(issue_url.strip())
    if not match:
        raise ValueError(
            "请输入 GitHub issue 网页 URL，格式类似: "
            "https://github.com/owner/repo/issues/123"
        )
    return match.group("owner"), match.group("repo"), match.group("number")


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-issue-description-fetcher",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API 请求失败: HTTP {exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"无法连接 GitHub: {exc.reason}") from exc


def slugify(value: str, fallback: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return slug[:80] or fallback


def build_markdown(issue: dict) -> str:
    body = issue.get("body") or ""
    title = issue.get("title") or "(no title)"
    author = (issue.get("user") or {}).get("login") or "(unknown)"
    source_url = issue.get("html_url") or ""
    created_at = issue.get("created_at") or ""

    parts = [
        f"# {title}",
        "",
        f"- Source: {source_url}",
        f"- Author: {author}",
        f"- Created: {created_at}",
        "",
        "## Original issue description",
        "",
        body.strip() or "_No description provided._",
        "",
    ]
    return "\n".join(parts)


def output_path_for(issue: dict, owner: str, repo: str, number: str, output: str | None) -> Path:
    if output:
        path = Path(output)
        if path.is_dir():
            title_slug = slugify(issue.get("title") or "", f"issue-{number}")
            return path / f"{owner}-{repo}-issue-{number}-{title_slug}.md"
        return path

    title_slug = slugify(issue.get("title") or "", f"issue-{number}")
    return Path(f"{owner}-{repo}-issue-{number}-{title_slug}.md")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch the author's description from a GitHub issue URL and save it as Markdown."
    )
    parser.add_argument("issue_url", nargs="?", help="GitHub issue URL")
    parser.add_argument(
        "-o",
        "--output",
        help="Output .md file path, or an output directory. Defaults to the current directory.",
    )
    args = parser.parse_args()

    issue_url = args.issue_url or input("GitHub issue URL: ").strip()
    owner, repo, number = parse_issue_url(issue_url)

    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{number}"
    issue = fetch_json(api_url)

    if "pull_request" in issue:
        print("Warning: this URL points to a pull request issue thread.", file=sys.stderr)

    output_path = output_path_for(issue, owner, repo, number, args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_markdown(issue), encoding="utf-8")

    print(f"Saved issue description to: {output_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
