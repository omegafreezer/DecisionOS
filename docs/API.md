# API examples

## Health
`GET /health`

## Decision workflow
`POST /api/decision`

Returns:
- decision id
- agent results
- trace
- evidence-backed actions

## Scenario
`POST /api/simulate`

```json
{
  "inventory_delta": 0.15,
  "price_delta": -0.05,
  "marketing_delta": 0.10
}
```

Values are relative changes, so `0.15` means +15%.
