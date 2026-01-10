"""
Seed script for RenewHub.

This script demonstrates:
- How to use the Flask app factory outside the request context
- How to work with SQLAlchemy sessions manually
- How Sites, Assets, and DailyMetrics relate
- How to insert structured, relational seed data

Run with:
    python scripts/seed_data.py
"""

from datetime import date, timedelta
from app import create_app, db
from app.models import Site, Asset, DailyMetric

app = create_app()

# Flask requires an application context when interacting with extensions like SQLAlchemy
with app.app_context():

    # Clear existing data (optional but useful during development)
    DailyMetric.query.delete()
    Asset.query.delete()
    Site.query.delete()
    db.session.commit()

    # --- 1. Create Sites -----------------------------------------------------
    site_uk = Site(
        name="Eastbourne Solar Farm",
        country="UK",
        latitude=50.77,
        longitude=0.28,
    )

    site_es = Site(
        name="Sevilla Wind Park",
        country="Spain",
        latitude=37.39,
        longitude=-5.99,
    )

    db.session.add_all([site_uk, site_es])
    db.session.commit()

    # --- 2. Create Assets ----------------------------------------------------
    # Assets belong to Sites via site_id

    asset_1 = Asset(
        name="Inverter A1",
        type="solar_inverter",
        site_id=site_uk.id,
        technology="solar",
        capacity_mw=0.5,
    )

    asset_2 = Asset(
        name="Panel Group B",
        type="solar_array",
        site_id=site_uk.id,
        technology="solar",
        capacity_mw=1.2,
    )

    asset_3 = Asset(
        name="Turbine T1",
        type="wind_turbine",
        site_id=site_es.id,
        technology="wind",
        capacity_mw=3.5,
    )


    db.session.add_all([asset_1, asset_2, asset_3])
    db.session.commit()

    # --- 3. Create Daily Metrics ---------------------------------------------
    # Metrics belong to Assets via asset_id
    # We'll generate 10 days of data for each asset

    metrics = []
    start = date.today() - timedelta(days=10)

    for i in range(10):
        metrics.append(
            DailyMetric(
            asset_id=asset_1.id,
            date=start + timedelta(days=i),
            energy_mwh=(120 + i * 3) / 1000.0,
            availability_pct=0.95 - (i * 0.005),  # example: 95% trending slightly down
            )
        )
    metrics.append(
        DailyMetric(
            asset_id=asset_2.id,
            date=start + timedelta(days=i),
            energy_mwh=(80 + i * 2) / 1000.0,
            availability_pct=0.97 - (i * 0.003),
            )
        )
    metrics.append(
        DailyMetric(
            asset_id=asset_3.id,
            date=start + timedelta(days=i),
            energy_mwh=(300 + i * 5) / 1000.0,
            availability_pct=0.92 + (i * 0.004),  # wind trending up
            )
        )

    db.session.add_all(metrics)
    db.session.commit()

    print("Seed complete.")
