#!/usr/bin/env python3
"""Emit deterministic nightly release metadata for GitHub workflows."""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path

from scripts.release_versions import parse_version, read_pyproject_version, write_github_outputs


def git_output(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.strip()


def nightly_metadata(root: Path, date_utc: str | None = None, commit_sha: str | None = None) -> dict[str, str]:
    date_token = date_utc or dt.datetime.now(dt.UTC).strftime("%Y%m%d")
    if len(date_token) != 8 or not date_token.isdigit():
        raise ValueError(f"invalid nightly date {date_token!r}; expected YYYYMMDD")

    sha = commit_sha or git_output(root, "rev-parse", "HEAD")
    if len(sha) < 7:
        raise ValueError(f"invalid commit sha {sha!r}")
    short_sha = sha[:7]

    current_version = parse_version(read_pyproject_version(root))
    base_version = current_version.base
    nightly_id = f"{date_token}-{short_sha}"
    immutable_tag = f"v{base_version}-nightly.{date_token}.{short_sha}"
    docker_version_tag = f"{base_version}-nightly.{date_token}-{short_sha}"
    helm_version = f"{base_version}-nightly.{date_token}+{short_sha}"

    return {
        "base_version": base_version,
        "commit_sha": sha,
        "short_sha": short_sha,
        "date_utc": date_token,
        "nightly_id": nightly_id,
        "immutable_tag": immutable_tag,
        "channel_tag": "nightly",
        "docker_version_tag": docker_version_tag,
        "helm_version": helm_version,
        "is_prerelease": "true",
        "package_index_policy": "skip-pypi",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--date-utc", default=None, help="override date token in YYYYMMDD")
    parser.add_argument("--commit-sha", default=None, help="override commit SHA")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    outputs = nightly_metadata(root, date_utc=args.date_utc, commit_sha=args.commit_sha)
    write_github_outputs(outputs)
    for key, value in outputs.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
