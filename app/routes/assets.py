from flask import request
from flask_smorest import Blueprint

from app.models import db, Asset

assets_bp = Blueprint("assets", __name__, url_prefix="/assets")


@assets_bp.get("/site/<int:site_id>")
def assets_for_site(site_id):
    assets = Asset.query.filter_by(site_id=site_id).all()
    return [a.to_dict() for a in assets]

@assets_bp.get("/")
def list_assets():
    assets = Asset.query.all()
    return [a.to_dict() for a in assets]

@assets_bp.post("/")
def create_asset():
    data = request.json
    asset = Asset(
        site_id=data["site_id"],
        name=data["name"],
        capacity_mw=data["capacity_mw"]
    )
    db.session.add(asset)
    db.session.commit()
    return asset.to_dict(), 201
