# Release Management Context

## Nightly channel workflow

Nightly releases are a separate, non-promoting channel built from `main` HEAD. They are intended for fast feedback and integration verification, not stable promotion.

Nightly automation:

- runs by schedule and manual dispatch
- runs release-confidence validation gates before publish
- computes deterministic nightly identifiers from UTC date and commit SHA
- publishes an immutable nightly tag and updates a movable `nightly` channel tag

## Artifact scope

Nightly publishes:

- Docker images tagged with immutable nightly identifier and `nightly`
- Helm chart package versioned for nightly
- GitHub prerelease metadata/install notes for the immutable nightly tag

Nightly does **not** publish to PyPI.

## Promotion boundaries

- Stable releases remain owned by release-please + stable release workflow.
- Beta releases remain owned by beta sync/publish workflows.
- Nightly does not retag or promote into stable aliases (`latest`, major, minor) and does not replace beta/stable governance.

## Rollback and reruns

- If a nightly run fails, rerun with `workflow_dispatch` against the same commit/date for idempotent recovery.
- Immutable tag collisions on a different commit fail closed and require operator intervention rather than unsafe overwrite.
