from flask import request
from flask_smorest import Blueprint
from app.models import db, Site

sites_bp = Blueprint("sites", __name__, url_prefix="/sites")


@sites_bp.get("/")
def list_sites():
    sites = Site.query.all()
    return [s.to_dict() for s in sites]

@sites_bp.post("/")
def create_site():
    data = request.json
    site = Site(
        name=data["name"],
        country=data["country"],
        latitude=data["latitude"],
        longitude=data["longitude"]
    )
    db.session.add(site)
    db.session.commit()
    return site.to_dict(), 201
