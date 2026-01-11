# Renew Hub Backend

A Flask + Postgres backend for renewable energy assets, daily metrics, and ETL ingestion.

## Features
- Flask API with modular blueprints
- Postgres database with SQLAlchemy models
- Seed pipeline for sites, assets, and daily metrics
- ETL ingestion endpoint
- Filtering, pagination, and nested routes

## Endpoints

### Sites
- `GET /sites/`
- `GET /sites/<id>`
- `GET /sites/<id>/assets`

### Assets
- `GET /assets/`
- `GET /assets/<id>`

### Metrics
- `GET /metrics/`
  - filters: `asset_id`, `site_id`, `start`, `end`
  - pagination: `page`, `limit`
- `GET /metrics/asset/<id>`
- `POST /etl/ingest`

## Running Locally

`flask run`

## Seeding the Database

`python scripts/create_db.py python -m scripts.seed_data`


