## Why

Adding a limit rule to an API key that already has request history should not
start that rule at zero. If it does, an operator can accidentally give the key a
fresh full window even though the key has already consumed tokens or cost inside
that window.

## What Changes

- Seed new API-key limit rules from existing request-log usage for the trailing
  current window ending at update time.
- Match seeded usage to the new rule's limit type and optional model filter.
- Keep brand-new keys or keys without matching historical usage at zero.
- Preserve existing truncation semantics for cost limits by storing
  microdollars with floor/truncate behavior.

## Impact

- API-key update behavior for newly added limit rules.
- Historical request-log aggregation used for API-key limit seeding.
