from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts.nightly_release_metadata import nightly_metadata


def init_git_repo(root: Path) -> str:
    subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
    (root / "pyproject.toml").write_text('[project]\nname = "codex-lb"\nversion = "1.20.2-beta.1"\n', encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=root, check=True, stdout=subprocess.PIPE)
    sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, stdout=subprocess.PIPE
    ).stdout.strip()
    return sha


def test_nightly_metadata_uses_base_version_and_deterministic_identifiers(tmp_path: Path) -> None:
    sha = init_git_repo(tmp_path)

    data = nightly_metadata(tmp_path, date_utc="20260707")

    assert data["base_version"] == "1.20.2"
    assert data["commit_sha"] == sha
    assert data["short_sha"] == sha[:7]
    assert data["nightly_id"] == f"20260707-{sha[:7]}"
    assert data["immutable_tag"] == f"v1.20.2-nightly.20260707.{sha[:7]}"
    assert data["docker_version_tag"] == f"1.20.2-nightly.20260707-{sha[:7]}"
    assert data["helm_version"] == f"1.20.2-nightly.20260707+{sha[:7]}"
    assert data["channel_tag"] == "nightly"
    assert data["package_index_policy"] == "skip-pypi"


def test_nightly_metadata_accepts_explicit_commit_override(tmp_path: Path) -> None:
    init_git_repo(tmp_path)

    data = nightly_metadata(tmp_path, date_utc="20260707", commit_sha="1234567890abcdef")

    assert data["commit_sha"] == "1234567890abcdef"
    assert data["short_sha"] == "1234567"
    assert data["nightly_id"] == "20260707-1234567"
    assert data["immutable_tag"] == "v1.20.2-nightly.20260707.1234567"


@pytest.mark.parametrize("bad_date", ["2026-07-07", "202607", "abc", ""])
def test_nightly_metadata_rejects_invalid_date_tokens(tmp_path: Path, bad_date: str) -> None:
    init_git_repo(tmp_path)
    with pytest.raises(ValueError):
        nightly_metadata(tmp_path, date_utc=bad_date)


def test_nightly_metadata_rejects_short_commit_sha(tmp_path: Path) -> None:
    init_git_repo(tmp_path)
    with pytest.raises(ValueError):
        nightly_metadata(tmp_path, date_utc="20260707", commit_sha="abc")
