from datetime import datetime
from flask import request
from flask_smorest import Blueprint

from app.utils.validation import ValidationError, validate_payload
from app.utils.query import parse_query_params

from app.models import db, DailyMetric

from app.schemas.metric import DailyMetricSchema


metrics_bp = Blueprint("metrics", __name__, url_prefix="/metrics")


# -----------------------------
# Helpers
# -----------------------------
def parse_date(value):
    try:
        return datetime.fromisoformat(value).date()
    except Exception:
        raise ValidationError(f"Invalid date: {value}")


# -----------------------------
# Routes
# -----------------------------

@metrics_bp.get("/")
def list_metrics():
    query = DailyMetric.query

    # --- Parse & validate query params ---
    filters = parse_query_params({
        "asset_id": int,
        "site_id": int,
        "start": "date",
        "end": "date",
        "page": int,
        "limit": int
    }, request.args)

    # --- Filtering ---
    if "asset_id" in filters:
        query = query.filter(DailyMetric.asset_id == filters["asset_id"])

    if "site_id" in filters:
        query = query.join(DailyMetric.asset).filter_by(site_id=filters["site_id"])

    if "start" in filters:
        query = query.filter(DailyMetric.date >= filters["start"])

    if "end" in filters:
        query = query.filter(DailyMetric.date <= filters["end"])

    # --- Pagination ---
    page = filters.get("page", 1)
    limit = filters.get("limit", 50)

    metrics = query.paginate(page=page, per_page=limit, error_out=False)

    return {
        "page": page,
        "limit": limit,
        "total": metrics.total,
        "items": [m.to_dict() for m in metrics.items]
    }


@metrics_bp.post("/")
def create_metric():
    data = request.json

    # Validate incoming payload
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

@metrics_bp.route("/asset/<int:asset_id>")
@metrics_bp.response(200, DailyMetricSchema(many=True))
def metrics_for_asset(asset_id):
    metrics = DailyMetric.query.filter_by(asset_id=asset_id).all()
    return metrics

