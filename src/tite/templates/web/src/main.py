"""
Main entry point for the web application.

This module sets up and runs the web server for the {{ project_name }}
application.
"""

import logging
import os
from pathlib import Path

# Try to import FastAPI first, fallback to Flask if not available
try:
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    import uvicorn
    FRAMEWORK = "fastapi"
except ImportError:
    from flask import Flask, render_template, request, jsonify, send_from_directory
    FRAMEWORK = "flask"

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log", mode="a", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

# Application settings
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "127.0.0.1")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
STATIC_DIR = PROJECT_ROOT / "src" / "static"
TEMPLATES_DIR = PROJECT_ROOT / "src" / "templates"


def create_app():
    """
    Create and configure the web application.
    
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
        title="{{ project_name }}",
        description="{{ project_description }}",
        version="0.1.0",
        debug=DEBUG,
    )
    
    # Setup templates
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    
    # Setup static files
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Home page."""
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "{{ project_name }}",
                "message": "Welcome to {{ project_name }}!",
                "framework": "FastAPI",
            },
        )
    
    @app.get("/health", response_class=JSONResponse)
    async def health():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "framework": "FastAPI",
            "version": "0.1.0",
        }
    
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def catch_all(path: str):
        """Catch-all for undefined routes."""
        return JSONResponse(
            status_code=404,
            content={"detail": f"Route '/{path}' not found"}
        )
    
    return app


def create_flask_app():
    """Create Flask application."""
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
        static_url_path="/static",
    )
    
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG
    
    @app.route("/")
    def home():
        """Home page."""
        return render_template(
            "index.html",
            title="{{ project_name }}",
            message="Welcome to {{ project_name }}!",
            framework="Flask",
        )
    
    @app.route("/health")
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "framework": "Flask",
            "version": "0.1.0",
        })
    
    return app


def main():
    """Run the web application."""
    logger.info("Starting {{ project_name }} web application...")
    logger.info(f"Framework: {FRAMEWORK}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"Server: http://{HOST}:{PORT}")
    
    app = create_app()
    
    if FRAMEWORK == "fastapi":
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