"""
Health checking for Tite.

This module provides health check functionality for monitoring
project health and status.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from tite.diagnostics.checks import CheckResult, CheckStatus


class HealthStatus(Enum):
    """Health status levels."""
    HEALTHY = "healthy"
    WARNING = "warning"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthReport:
    """
    Health report for a project.
    
    Attributes:
        timestamp: Report timestamp
        status: Overall health status
        checks: List of check results
        summary: Summary information
        recommendations: List of recommendations
    """
    timestamp: datetime = field(default_factory=datetime.now)
    status: HealthStatus = HealthStatus.UNKNOWN
    checks: List[CheckResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "checks": [c.to_dict() for c in self.checks],
            "summary": self.summary,
            "recommendations": self.recommendations,
        }


class HealthChecker:
    """
    Checks the health of a Tite project.
    
    This class provides health monitoring for projects, including
    periodic checks and status reporting.
    
    Attributes:
        project_path: Path to the project
        checks: List of health checks
        report: Current health report
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize the health checker.
        
        Args:
            project_path: Path to the project
        """
        self.project_path = Path(project_path)
        self.checks: List[Check] = []
        self.report: Optional[HealthReport] = None
        self._register_checks()
        
    def _register_checks(self) -> None:
        """Register health checks."""
        from tite.diagnostics.checks import (
            PythonCheck,
            VenvCheck,
            GitCheck,
            ProjectFilesCheck,
            DependenciesCheck,
            ConfigCheck,
        )
        
        self.checks = [
            PythonCheck(self.project_path),
            VenvCheck(self.project_path),
            GitCheck(self.project_path),
            ProjectFilesCheck(self.project_path),
            DependenciesCheck(self.project_path),
            ConfigCheck(self.project_path),
        ]
        
    def check_health(self) -> HealthReport:
        """
        Run all health checks.
        
        Returns:
            HealthReport: Health report
        """
        results = []
        recommendations = []
        
        for check in self.checks:
            result = check.run()
            results.append(result)
            
            if result.status == CheckStatus.FAILED:
                recommendations.extend(result.recommendations)
                
        # Determine overall status
        status = self._determine_status(results)
        
        # Create report
        self.report = HealthReport(
            status=status,
            checks=results,
            summary=self._create_summary(results),
            recommendations=recommendations,
        )
        
        return self.report
        
    def _determine_status(self, results: List[CheckResult]) -> HealthStatus:
        """
        Determine overall health status.
        
        Args:
            results: List of check results
            
        Returns:
            HealthStatus: Overall health status
        """
        failed = any(r.status == CheckStatus.FAILED for r in results)
        warnings = any(r.status == CheckStatus.WARNING for r in results)
        
        if failed:
            return HealthStatus.UNHEALTHY
        elif warnings:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
            
    def _create_summary(self, results: List[CheckResult]) -> Dict[str, Any]:
        """
        Create a summary of check results.
        
        Args:
            results: List of check results
            
        Returns:
            Dict[str, Any]: Summary information
        """
        total = len(results)
        passed = sum(1 for r in results if r.status == CheckStatus.PASSED)
        warnings = sum(1 for r in results if r.status == CheckStatus.WARNING)
        failed = sum(1 for r in results if r.status == CheckStatus.FAILED)
        
        return {
            "total": total,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
        }
        
    def get_status(self) -> HealthStatus:
        """
        Get the current health status.
        
        Returns:
            HealthStatus: Current health status
        """
        if self.report:
            return self.report.status
            
        # Run checks if no report
        report = self.check_health()
        return report.status
        
    def get_issues(self) -> List[Dict[str, Any]]:
        """
        Get all issues found by health checks.
        
        Returns:
            List[Dict[str, Any]]: List of issues
        """
        issues = []
        
        if self.report:
            for result in self.report.checks:
                if result.status == CheckStatus.FAILED:
                    issues.append({
                        "check": result.check_name,
                        "message": result.message,
                        "details": result.details,
                        "recommendations": result.recommendations,
                    })
                    
        return issues
        
    def get_warnings(self) -> List[Dict[str, Any]]:
        """
        Get all warnings from health checks.
        
        Returns:
            List[Dict[str, Any]]: List of warnings
        """
        warnings = []
        
        if self.report:
            for result in self.report.checks:
                if result.status == CheckStatus.WARNING:
                    warnings.append({
                        "check": result.check_name,
                        "message": result.message,
                        "details": result.details,
                    })
                    
        return warnings
        
    def is_healthy(self) -> bool:
        """
        Check if the project is healthy.
        
        Returns:
            bool: True if healthy
        """
        status = self.get_status()
        return status == HealthStatus.HEALTHY