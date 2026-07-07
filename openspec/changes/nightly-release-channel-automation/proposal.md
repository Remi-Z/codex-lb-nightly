# Change: Nightly release channel automation

## Problem

The repository has stable and beta release automation, but no first-class nightly channel. Operators currently lack an automated nightly path that validates main, produces reproducible nightly identifiers, and publishes channel-scoped artifacts without interfering with stable or beta ownership.

## Solution

- Add a dedicated nightly GitHub Actions workflow that runs on schedule and manual dispatch, gates on local-equivalent CI checks, and publishes nightly artifacts from `main`.
- Add deterministic nightly metadata helpers for date+SHA identifiers and immutable nightly tags.
- Publish nightly Docker, Helm, and GitHub prerelease artifacts while explicitly skipping PyPI for nightly builds.
- Document local validation/toolchain expectations and nightly operator flow in OpenSpec context docs.

## Changes

- New nightly metadata helper script with unit tests
- New nightly release workflow (`.github/workflows/nightly-release.yml`)
- OpenSpec requirements for nightly triggers, tagging, retention/idempotency, and guardrails
- README development guidance aligned with canonical `make ci-fast` and `make ci` gates

## Out of scope

- Changing stable release ownership (release-please remains stable owner)
- Changing beta release preparation/publish flows
- Promoting nightly artifacts to stable tags or release aliases
