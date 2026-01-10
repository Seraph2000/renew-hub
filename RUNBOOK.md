# renew-hub RUNBOOK

## 1. Create and activate your virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows equivalent:

```bash
venv\Scripts\activate
```

## 2. Install dependencies

In your project root:

```bash
pip install flask flask_sqlalchemy psycopg2-binary python-dotenv
```

Or add to `requirements.txt`:

```
Flask
Flask-SQLAlchemy
psycopg2-binary
boto3
python-dotenv
```

## 3. Create .env file

In project root:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/renewhub
```

Everything in .env is a string — no quotes needed.


## 4. Create docker-compose.yml

Place this in your project root:

```yaml
version: "3.9"

services:
  db:
    image: postgres:15
    container_name: renewhub-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: renewhub
    ports:
      - "5432:5432"
    volumes:
      - renewhub_data:/var/lib/postgresql/data

volumes:
  renewhub_data:
```

## 5. Start Postgres using Docker Compose

From project root:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

You should see:

```bash
renewhub-db   postgres:15   Up
```

## 6. Add .env loading to your DB creation script

At the top of scripts/create_db.py:

```python
from dotenv import load_dotenv
load_dotenv()
```

This ensures SQLAlchemy sees your DATABASE_URL.

## 7. Ensure Python can see your project root

From project root:

```bash
export PYTHONPATH=$(pwd)
```

_(Windows PowerShell equivalent: $env:PYTHONPATH = (Get-Location))_

## 8. Create database tables

```bash
python scripts/create_db.py
```

Expected output:

```bash
Database tables created.
```

## 9. Verify tables inside Postgres

Enter the DB:

```bash
docker exec -it renewhub-db psql -U postgres -d renewhub
```

List tables:

```bash
\dt
```

You should see:

```bash
sites
assets
daily_metrics
```

Exit:

```bash
\q
```

## 10. Run the Flask app

From project root:

```bash
export FLASK_APP=app
flask run
```

Test:

```bash
curl http://127.0.0.1:5000/health
```

Expected:

```bash
{"status": "ok"}
```