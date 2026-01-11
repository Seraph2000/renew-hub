# Verification Runbook

## ETL Ingestion Verification

This runbook validates that the ETL ingestion endpoint (POST /etl/ingest) is functioning correctly after code changes, schema updates, or seed resets. It ensures that the backend can reliably accept, validate, and persist incoming metric data.

## ✅ Checklist

- [ ] Restart backend cleanly  
- [ ] Confirm `/health` responds  
- [ ] Verify existing metrics  
- [ ] Send test ingestion payload  
- [ ] Confirm new metric appears  
- [ ] Validate DB persistence (optional)  
- [ ] Test error handling  
- [ ] Confirm filtering still works  
- [ ] Confirm pagination still works  

---

### 1. Restart the backend cleanly

A clean restart ensures all code changes and environment variables are loaded.

`wsl --shutdown`

Reopen your terminal:

`flask run`


Expected:
- Flask starts without errors
- SQLAlchemy connects to the database
- Blueprints register successfully

### 2. Confirm the API is reachable

`curl http://127.0.0.1:5000/health`


Expected:

`{"status": "ok"}`


If this fails, the app factory or environment variables need attention.

### 3. Verify existing metrics before ingestion

This establishes a baseline.

```bash
curl http://127.0.0.1:5000/metrics/?asset_id=1
```

Expected:
- A list of existing metrics
- No 500 errors
- Dates in ISO format

### 4. Send a test ingestion payload

This simulates what your future ETL pipeline will do.

```bash
curl -X POST http://127.0.0.1:5000/etl/ingest \
  -H "Content-Type: application/json" \
  -d '{
        "asset_id": 1,
        "date": "2026-01-10",
        "energy_mwh": 0.222,
        "availability_pct": 0.88
      }'
```

Expected:

- HTTP 201 Created
- JSON body containing the newly inserted metric
- No stack traces in the Flask console

If you see a 400 or 500, check:

- field names
- date format
- model constraints
- DB session rollback messages

### 5. Confirm the new metric appears in the database

Query the API:

```bash
curl http://127.0.0.1:5000/metrics/?asset_id=1
```


Expected:

- The new metric appears at the end of the list
- Values match the payload
- No duplicates unless intentionally inserted

Optional deeper check:

```bash
curl "http://127.0.0.1:5000/metrics/?asset_id=1&start=2026-01-10&end=2026-01-10"
```


### 6. Validate DB persistence directly (optional but recommended)

If using Docker:

`docker exec -it renewhub-db psql -U postgres -d renewhub`


Then:

`SELECT * FROM daily_metrics WHERE date = '2026-01-10';`


Expected:

- Exactly one row
- Values match the ingestion payload

### 7. Test error handling (optional)

Send an invalid payload:

```bash
curl -X POST http://127.0.0.1:5000/etl/ingest \
  -H "Content-Type: application/json" \
  -d '{}'
```

Expected:

- HTTP 400
- JSON error message
- No server crash

This confirms your rollback logic is working.

### 8. Confirm filtering still works after ingestion

`curl "http://127.0.0.1:5000/metrics/?start=2026-01-10&end=2026-01-10"`


Expected:

- Only the newly ingested metric
- No pagination errors
- No filtering regressions

9. Confirm pagination still works

`curl "http://127.0.0.1:5000/metrics/?page=1&limit=5"`


Expected:

- JSON structure with page, limit, total, and items
- No errors from .paginate()



