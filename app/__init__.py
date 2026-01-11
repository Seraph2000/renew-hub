from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register blueprints
    from app.routes.sites import sites_bp
    from app.routes.assets import assets_bp
    from app.routes.metrics import metrics_bp
    from app.routes.etl import etl_bp

    app.register_blueprint(sites_bp, url_prefix="/sites")
    app.register_blueprint(assets_bp, url_prefix="/assets")
    app.register_blueprint(metrics_bp, url_prefix="/metrics")
    app.register_blueprint(etl_bp, url_prefix="/etl")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app
