from datetime import date
from flask_sqlalchemy import SQLAlchemy

from app import db

class Site(db.Model):
    __tablename__ = "sites"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Relationship: one site → many assets
    assets = db.relationship("Asset", back_populates="site", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Site {self.id} {self.name}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude
        }



class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey("sites.id"), nullable=False)
    technology = db.Column(db.String(20), nullable=False)  # solar | wind | battery
    capacity_mw = db.Column(db.Float, nullable=False)

    # Relationship: many assets → one site
    site = db.relationship("Site", back_populates="assets")

    # Relationship: one asset → many metrics
    metrics = db.relationship("DailyMetric", back_populates="asset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Asset {self.id} {self.technology}>"
    
    def to_dict(self):
        return {
        "id": self.id,
        "site_id": self.site_id,
        "name": self.name,
        "type": self.type,
        "technology": self.technology,
        "capacity_mw": self.capacity_mw,
        }



class DailyMetric(db.Model):
    __tablename__ = "daily_metrics"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    energy_mwh = db.Column(db.Float, nullable=False)
    availability_pct = db.Column(db.Float, nullable=False)

    # Relationship: many metrics → one asset
    asset = db.relationship("Asset", back_populates="metrics")

    __table_args__ = (
        db.UniqueConstraint("asset_id", "date", name="uq_asset_date"),
    )

    def __repr__(self):
        return f"<DailyMetric asset={self.asset_id} date={self.date}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "asset_id": self.asset_id,
            "date": self.date.isoformat(),
            "energy_mwh": self.energy_mwh,
            "availability_pct": self.availability_pct,
        }

