# release-management Specification Delta

## ADDED Requirements

### Requirement: Nightly release workflow runs on schedule and manual dispatch

The repository SHALL provide a dedicated nightly release workflow that runs on a nightly schedule and via manual dispatch. The workflow SHALL build from `main` HEAD and SHALL run release-confidence validation gates before publishing nightly artifacts.

#### Scenario: Scheduled nightly run validates then publishes

- **GIVEN** the nightly schedule triggers the workflow
- **WHEN** nightly validation gates pass on `main` HEAD
- **THEN** the workflow publishes nightly channel artifacts
- **AND** stable and beta workflows remain unchanged

#### Scenario: Manual nightly rerun/backfill

- **GIVEN** an operator runs the nightly workflow via `workflow_dispatch`
- **WHEN** required validation gates pass
- **THEN** the workflow publishes the same channel-scoped artifacts for the target commit

### Requirement: Nightly release identifiers are deterministic and idempotent

Nightly automation SHALL derive deterministic nightly metadata from UTC date and commit SHA. It SHALL publish an immutable nightly Git tag and a movable `nightly` channel tag. Re-runs for the same commit/date SHALL be idempotent and SHALL fail closed if an immutable nightly tag already exists on a different commit.

#### Scenario: Immutable nightly tag already exists on the same commit

- **GIVEN** the workflow computes immutable nightly tag `vX.Y.Z-nightly.YYYYMMDD.<sha7>`
- **AND** that tag already points to the target commit
- **WHEN** the workflow reruns
- **THEN** it reuses the existing immutable tag without creating conflicts

#### Scenario: Immutable nightly tag collides with a different commit

- **GIVEN** immutable nightly tag `vX.Y.Z-nightly.YYYYMMDD.<sha7>` exists
- **AND** it points to a commit other than the target commit
- **WHEN** the workflow attempts publish
- **THEN** the workflow fails before publishing artifacts

### Requirement: Nightly artifact publishing is channel-scoped and non-promoting

Nightly releases SHALL publish channel-scoped Docker and Helm artifacts and a GitHub prerelease with nightly install metadata. Nightly automation SHALL NOT publish to PyPI and SHALL NOT mutate stable aliases (`latest`, `X`, `X.Y`) or stable/beta release ownership boundaries.

#### Scenario: Nightly publish skips PyPI and keeps stable/beta ownership

- **GIVEN** a nightly workflow run publishes artifacts
- **WHEN** publish steps complete
- **THEN** Docker includes immutable nightly tag and `nightly` channel tag only
- **AND** Helm publishes a nightly chart version
- **AND** GitHub prerelease is created or updated for the immutable nightly tag
- **AND** no PyPI publish step is executed
- **AND** stable and beta release ownership remains unchanged
