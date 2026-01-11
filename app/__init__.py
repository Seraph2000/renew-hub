from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from app.utils.validation import ValidationError
from app.utils.errors import error_response


import os

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # OpenAPI / Swagger config
    app.config["API_TITLE"] = "RenewHub API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_REDOC_PATH"] = "/redoc"
    app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"

    db.init_app(app)

    # Create the Smorest API wrapper
    api = Api(app)

    # Register blueprints
    from app.routes.sites import sites_bp
    from app.routes.assets import assets_bp
    from app.routes.metrics import metrics_bp
    from app.routes.etl import etl_bp


    # Register blueprints on the API wrapper
    
    api.register_blueprint(sites_bp)
    api.register_blueprint(assets_bp)
    api.register_blueprint(metrics_bp)
    api.register_blueprint(etl_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}
    
    register_error_handlers(app)

    return app

def register_error_handlers(app):

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        # Roll back the failed transaction
        db.session.rollback()

        if "uq_asset_date" in str(err.orig):
            return error_response(
                "unique_constraint",
                "Metric for this asset and date already exists",
                409
            )

        return error_response(
            "integrity_error",
            "Database integrity error",
            400
        )


    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return error_response(
        "validation_error",
        err.message,
        err.status
    )


    @app.errorhandler(404)
    def handle_404(err):
        return error_response(
            "not_found",
            "Resource not found",
            404
        )


    @app.errorhandler(500)
    def handle_500(err):
        return error_response(
            "server_error",
            "Internal server error",
            500
        )


