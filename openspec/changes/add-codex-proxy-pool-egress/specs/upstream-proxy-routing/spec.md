## ADDED Requirements

### Requirement: Account-bound upstream traffic must use the bound proxy pool
When an account has an explicit upstream proxy pool binding, every ChatGPT/OpenAI/Codex upstream operation using that account's credentials MUST resolve a route from the bound pool before opening a network connection.

#### Scenario: Bound pool unavailable fails closed
- **GIVEN** an account has an explicit upstream proxy pool binding
- **AND** the bound pool has no active usable endpoint
- **WHEN** an account-scoped ChatGPT upstream operation is attempted
- **THEN** the operation MUST fail before opening an upstream network connection
- **AND** it MUST NOT use the default pool, environment proxy, or direct egress.

### Requirement: Codex upstream Codex client must require a resolved route and built-in TLS fingerprint
Affected Codex upstream HTTP and websocket calls MUST use the Codex upstream client with an explicit resolved route and the built-in Codex CLI TLS fingerprint.

#### Scenario: Runtime fingerprint override rejected
- **WHEN** a caller attempts to pass runtime fingerprint kwargs such as `impersonate`, `ja3`, `akamai`, or `extra_fp`
- **THEN** the client MUST reject the call before opening a network connection.

### Requirement: Route metadata must be persisted for migrated upstream calls
Request logs for migrated upstream calls MUST record route mode, proxy pool id, proxy endpoint id, same-pool fallback use, and fail-closed reason where applicable.

#### Scenario: Fail-closed reason recorded
- **GIVEN** route resolution fails closed before network open
- **WHEN** the request log is written
- **THEN** the log MUST include the fail-closed reason without proxy credentials.
