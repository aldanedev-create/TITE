"""
Health check routes for the API.

This module provides health check endpoints for monitoring
and readiness probes.
"""

import os
import sys
from datetime import datetime
from typing import Any, Dict

# Try to import FastAPI first
try:
    from fastapi import APIRouter, status
    from fastapi.responses import JSONResponse
    FRAMEWORK = "fastapi"
except ImportError:
    from flask import Blueprint, jsonify
    FRAMEWORK = "flask"


def get_system_info() -> Dict[str, Any]:
    """
    Get system information for health check.
    
    Returns:
        Dict[str, Any]: System information
    """
    return {
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "cwd": os.getcwd(),
        "environment": os.getenv("APP_ENV", "development"),
    }


def get_dependencies_status() -> Dict[str, bool]:
    """
    Check status of dependencies.
    
    Returns:
        Dict[str, bool]: Dependency status
    """
    status = {}
    
    # Check database
    try:
        # Import and test database connection
        # This is a placeholder - implement actual checks
        status["database"] = True
    except Exception:
        status["database"] = False
    
    # Check Redis
    try:
        # Import and test Redis connection
        # This is a placeholder - implement actual checks
        status["redis"] = True
    except Exception:
        status["redis"] = False
    
    return status


def get_health_response() -> Dict[str, Any]:
    """
    Generate health check response.
    
    Returns:
        Dict[str, Any]: Health check response
    """
    dependencies = get_dependencies_status()
    all_healthy = all(dependencies.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "0.1.0",
        "service": "{{ project_name }} API",
        "dependencies": dependencies,
        "system": get_system_info(),
    }


# FastAPI Router
if FRAMEWORK == "fastapi":
    router = APIRouter()
    
    @router.get("/health", status_code=status.HTTP_200_OK)
    @router.get("/health/live", status_code=status.HTTP_200_OK)
    @router.get("/health/ready", status_code=status.HTTP_200_OK)
    async def health_check():
        """
        Health check endpoint.
        
        Returns:
            JSONResponse: Health status
        """
        response = get_health_response()
        status_code = 200 if response["status"] == "healthy" else 503
        return JSONResponse(content=response, status_code=status_code)
    
    @router.get("/health/dependencies")
    async def dependencies_check():
        """
        Dependencies health check.
        
        Returns:
            JSONResponse: Dependencies status
        """
        return JSONResponse(content={"dependencies": get_dependencies_status()})
    
    @router.get("/ping")
    async def ping():
        """
        Simple ping endpoint.
        
        Returns:
            JSONResponse: Pong response
        """
        return JSONResponse(content={"ping": "pong", "timestamp": datetime.utcnow().isoformat() + "Z"})


# Flask Blueprint
else:
    blueprint = Blueprint("health", __name__)
    
    @blueprint.route("/health", methods=["GET"])
    @blueprint.route("/health/live", methods=["GET"])
    @blueprint.route("/health/ready", methods=["GET"])
    def health_check():
        """
        Health check endpoint.
        """
        response = get_health_response()
        status_code = 200 if response["status"] == "healthy" else 503
        return jsonify(response), status_code
    
    @blueprint.route("/health/dependencies", methods=["GET"])
    def dependencies_check():
        """
        Dependencies health check.
        """
        return jsonify({"dependencies": get_dependencies_status()})
    
    @blueprint.route("/ping", methods=["GET"])
    def ping():
        """
        Simple ping endpoint.
        """
        return jsonify({"ping": "pong", "timestamp": datetime.utcnow().isoformat() + "Z"})