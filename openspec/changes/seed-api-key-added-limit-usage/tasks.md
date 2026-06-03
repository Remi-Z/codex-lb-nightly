## 1. Spec

- [x] 1.1 Document that newly added API-key limit rules seed current usage from
  existing request logs.
- [x] 1.2 Cover model-filtered token limits and cost-limit microdollar
  truncation semantics.

## 2. Implementation

- [x] 2.1 Add historical request-log aggregation for current-window API-key
  limit usage.
- [x] 2.2 Use the historical aggregate when adding a new limit rule to an
  existing API key.

## 3. Verification

- [x] 3.1 Run API-key repository unit tests.
- [x] 3.2 Validate the OpenSpec change.
