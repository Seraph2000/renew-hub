from flask import Blueprint, request, jsonify
from app.models import db, DailyMetric

metrics_bp = Blueprint("metrics", __name__)

@metrics_bp.get("/")
def list_metrics():
    metrics = DailyMetric.query.all()
    return jsonify([m.to_dict() for m in metrics])

@metrics_bp.post("/")
def create_metric():
    data = request.json
    metric = DailyMetric(
        asset_id=data["asset_id"],
        date=data["date"],
        energy_mwh=data["energy_mwh"]
    )
    db.session.add(metric)
    db.session.commit()
    return metric.to_dict(), 201
