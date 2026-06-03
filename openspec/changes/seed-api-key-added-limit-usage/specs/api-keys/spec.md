## MODIFIED Requirements

### Requirement: API key limit updates preserve usage

When updating API key limits, the system SHALL preserve existing usage state
(`current_value`, `reset_at`) for unchanged limit rules. Limit comparison key is
`(limit_type, limit_window, model_filter)`.

- Matching existing rule: `current_value` and `reset_at` SHALL be preserved;
  only `max_value` is updated.
- New rule on an existing API key: fresh `reset_at` SHALL be created and
  `current_value` SHALL be seeded from the API key's existing request-log usage
  inside the trailing current window ending at update time, using the new rule's
  type and optional `model_filter`.
- New rule on a brand-new API key with no matching request logs:
  `current_value=0`.
- Removed rule (in existing but not in update): row is deleted.

Usage reset SHALL only occur via an explicit action (`reset_usage` field or
dedicated endpoint), never as a side-effect of metadata or policy edits.

#### Scenario: New rule seeds current window usage for an already-used key

- **WHEN** an API key PATCH adds a new limit rule to a key that already has
  request logs in the current limit window
- **THEN** the new rule gets a fresh `reset_at`
- **AND** its `current_value` equals the matching current-window request-log
  usage for that key and rule

#### Scenario: Cost limit seeding uses microdollar truncation

- **WHEN** an API key PATCH adds a cost limit to a key with request-log cost
  history in the current limit window
- **THEN** the seeded `current_value` is the sum of each matching
  `cost_usd * 1_000_000` value truncated toward zero
  before integer storage
