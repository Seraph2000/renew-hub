from flask import Blueprint, request, jsonify
from app.models import db, DailyMetric
from datetime import datetime

from app.utils.validation import validate_payload, ValidationError


etl_bp = Blueprint("etl", __name__)

@etl_bp.post("/ingest")
def ingest_metric():
    data = request.json

    validate_payload(data, {
        "asset_id": int,
        "date": "date",
        "energy_mwh": float,
        "availability_pct": float
    })

    metric = DailyMetric(
        asset_id=data["asset_id"],
        date=datetime.fromisoformat(data["date"]).date(),
        energy_mwh=data["energy_mwh"],
        availability_pct=data["availability_pct"]
    )

    db.session.add(metric)
    db.session.commit()

    return metric.to_dict(), 201

