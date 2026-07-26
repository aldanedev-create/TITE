"""
Main entry point for the API application.

This module sets up and runs the REST API server for the {{ project_name }}
application.
"""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

# Try to import FastAPI first, fallback to Flask if not available
try:
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException
    FRAMEWORK = "fastapi"
except ImportError:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    FRAMEWORK = "flask"

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/api.log", mode="a", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

# Application settings
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "127.0.0.1")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
PROJECT_ROOT = Path(__file__).parent.parent.absolute()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting {{ project_name }} API...")
    logger.info(f"Framework: {FRAMEWORK}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"API Prefix: {API_PREFIX}")
    logger.info(f"Server: http://{HOST}:{PORT}")
    yield
    # Shutdown
    logger.info("Shutting down {{ project_name }} API...")


def create_app():
    """
    Create and configure the API application.
    
    Returns:
        FastAPI or Flask application instance
    """
    if FRAMEWORK == "fastapi":
        return create_fastapi_app()
    else:
        return create_flask_app()


def create_fastapi_app():
    """Create FastAPI application."""
    app = FastAPI(
        title="{{ project_name }} API",
        description="{{ project_description }}",
        version="0.1.0",
        debug=DEBUG,
        lifespan=lifespan,
        docs_url=f"{API_PREFIX}/docs",
        redoc_url=f"{API_PREFIX}/redoc",
        openapi_url=f"{API_PREFIX}/openapi.json",
    )
    
    # Configure CORS
    allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Import and register routes
    from src.routes import health
    app.include_router(health.router, prefix=API_PREFIX, tags=["health"])
    
    # Example: Import other routes as they are created
    # from src.routes import example
    # app.include_router(example.router, prefix=API_PREFIX, tags=["example"])
    
    # Exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                    "type": "http_error",
                }
            },
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            })
        
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": 422,
                    "message": "Validation error",
                    "type": "validation_error",
                    "details": errors,
                }
            },
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": 500,
                    "message": "Internal server error",
                    "type": "internal_error",
                }
            },
        )
    
    return app


def create_flask_app():
    """Create Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG
    
    # Configure CORS
    CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","))
    
    # Register routes
    from src.routes import health
    app.register_blueprint(health.blueprint, url_prefix=API_PREFIX)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": {
                "code": 404,
                "message": "Resource not found",
                "type": "not_found",
            }
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": {
                "code": 400,
                "message": "Bad request",
                "type": "bad_request",
            }
        }), 400
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal error: {error}")
        return jsonify({
            "error": {
                "code": 500,
                "message": "Internal server error",
                "type": "internal_error",
            }
        }), 500
    
    return app


def main():
    """Run the API application."""
    app = create_app()
    
    if FRAMEWORK == "fastapi":
        import uvicorn
        uvicorn.run(
            app,
            host=HOST,
            port=PORT,
            log_level="debug" if DEBUG else "info",
            reload=DEBUG,
        )
    else:
        app.run(
            host=HOST,
            port=PORT,
            debug=DEBUG,
        )


if __name__ == "__main__":
    main()