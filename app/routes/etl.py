from flask import Blueprint, request, jsonify
from app.models import db, DailyMetric
from datetime import date

etl_bp = Blueprint("etl", __name__)

@etl_bp.post("/ingest")
def ingest_metric():
    data = request.json

    try:
        metric = DailyMetric(
            asset_id=data["asset_id"],
            date=date.fromisoformat(data["date"]),
            energy_mwh=data["energy_mwh"],
            availability_pct=data["availability_pct"]
        )

        db.session.add(metric)
        db.session.commit()

        return jsonify(metric.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
