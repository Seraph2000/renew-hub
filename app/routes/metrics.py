from flask import Blueprint, request, jsonify
from app.models import db, DailyMetric

metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.get("/asset/<int:asset_id>")
def metrics_for_asset(asset_id):
    metrics = DailyMetric.query.filter_by(asset_id=asset_id).all()
    return jsonify([m.to_dict() for m in metrics])

@metrics_bp.get("/")
def list_metrics():
    query = DailyMetric.query

    asset_id = request.args.get("asset_id")
    site_id = request.args.get("site_id")
    start = request.args.get("start")
    end = request.args.get("end")

    if asset_id:
        query = query.filter(DailyMetric.asset_id == asset_id)

    if site_id:
        query = query.join(DailyMetric.asset).filter_by(site_id=site_id)

    if start:
        query = query.filter(DailyMetric.date >= start)

    if end:
        query = query.filter(DailyMetric.date <= end)

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=50, type=int)

    metrics = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "page": page,
        "limit": limit,
        "total": metrics.total,
        "items": [m.to_dict() for m in metrics.items]
    })


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
