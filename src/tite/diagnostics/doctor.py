"""
Doctor module for Tite.

This module provides the main doctor functionality for diagnosing
and fixing issues in Tite projects.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from tite.diagnostics.checks import (
    Check,
    CheckResult,
    CheckStatus,
    PythonCheck,
    VenvCheck,
    GitCheck,
    ProjectFilesCheck,
    DependenciesCheck,
    ConfigCheck,
)
from tite.diagnostics.report import ReportGenerator
from tite.exceptions import ConfigurationError


class Doctor:
    """
    Diagnoses and fixes issues in Tite projects.
    
    This class runs a series of health checks on a project and
    provides recommendations for fixing any issues found.
    
    Attributes:
        project_path: Path to the project
        checks: List of checks to run
        results: Results of checks
        verbose: Whether to show detailed output
    """
    
    def __init__(self, project_path: Path, verbose: bool = False):
        """
        Initialize the doctor.
        
        Args:
            project_path: Path to the project
            verbose: Whether to show detailed output
        """
        self.project_path = Path(project_path)
        self.verbose = verbose
        self.checks: List[Check] = []
        self.results: List[CheckResult] = []
        self._register_checks()
        
    def _register_checks(self) -> None:
        """Register all available checks."""
        self.checks = [
            PythonCheck(self.project_path),
            VenvCheck(self.project_path),
            GitCheck(self.project_path),
            ProjectFilesCheck(self.project_path),
            DependenciesCheck(self.project_path),
            ConfigCheck(self.project_path),
        ]
        
    def run_all_checks(self) -> List[CheckResult]:
        """
        Run all registered checks.
        
        Returns:
            List[CheckResult]: Results of all checks
        """
        self.results = []
        
        for check in self.checks:
            logger.debug(f"Running check: {check.name}")
            result = check.run()
            self.results.append(result)
            
            if self.verbose:
                self._print_check_result(result)
                
        return self.results
        
    def run_check(self, check_name: str) -> Optional[CheckResult]:
        """
        Run a specific check by name.
        
        Args:
            check_name: Name of the check to run
            
        Returns:
            Optional[CheckResult]: Result of the check or None
        """
        for check in self.checks:
            if check.name == check_name:
                result = check.run()
                self.results.append(result)
                return result
        return None
        
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all check results.
        
        Returns:
            Dict[str, Any]: Summary information
        """
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == CheckStatus.PASSED)
        warnings = sum(1 for r in self.results if r.status == CheckStatus.WARNING)
        failed = sum(1 for r in self.results if r.status == CheckStatus.FAILED)
        
        status = "healthy"
        if failed > 0:
            status = "unhealthy"
        elif warnings > 0:
            status = "warning"
            
        return {
            "total": total,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "status": status,
            "results": [r.to_dict() for r in self.results],
        }
        
    def fix_issues(self) -> bool:
        """
        Attempt to fix issues found by checks.
        
        Returns:
            bool: True if all issues were fixed
        """
        fixed_all = True
        
        for result in self.results:
            if result.status == CheckStatus.FAILED:
                logger.info(f"Attempting to fix: {result.check_name}")
                
                # Try to find the check that produced this result
                for check in self.checks:
                    if check.name == result.check_name and hasattr(check, "fix"):
                        try:
                            check.fix()
                            logger.info(f"Fixed: {result.check_name}")
                        except Exception as e:
                            logger.error(f"Failed to fix {result.check_name}: {e}")
                            fixed_all = False
                        break
                else:
                    logger.warning(f"No fix available for: {result.check_name}")
                    fixed_all = False
                    
        return fixed_all
        
    def _print_check_result(self, result: CheckResult) -> None:
        """
        Print a check result.
        
        Args:
            result: Check result to print
        """
        from tite.cli.output import console
        
        status_icons = {
            CheckStatus.PASSED: "✅",
            CheckStatus.WARNING: "⚠️",
            CheckStatus.FAILED: "❌",
            CheckStatus.SKIPPED: "⏭️",
        }
        
        status_colors = {
            CheckStatus.PASSED: "green",
            CheckStatus.WARNING: "yellow",
            CheckStatus.FAILED: "red",
            CheckStatus.SKIPPED: "dim",
        }
        
        icon = status_icons.get(result.status, "❓")
        color = status_colors.get(result.status, "white")
        
        console.print(f"[{color}]{icon} {result.check_name}[/{color}]")
        if result.message:
            console.print(f"  {result.message}")
        if self.verbose and result.details:
            for key, value in result.details.items():
                console.print(f"  [dim]{key}: {value}[/dim]")
        console.print()
        
    def generate_report(self, format: str = "text") -> str:
        """
        Generate a diagnostic report.
        
        Args:
            format: Report format (text, json, markdown)
            
        Returns:
            str: Report content
        """
        from tite.diagnostics.report import ReportGenerator, ReportFormat
        
        if not self.results:
            self.run_all_checks()
            
        format_map = {
            "text": ReportFormat.TEXT,
            "json": ReportFormat.JSON,
            "markdown": ReportFormat.MARKDOWN,
            "html": ReportFormat.HTML,
        }
        
        report_format = format_map.get(format, ReportFormat.TEXT)
        generator = ReportGenerator(report_format)
        return generator.generate(self.results, self.project_path)
        
    def save_report(self, output_path: Path, format: str = "text") -> None:
        """
        Save a diagnostic report to a file.
        
        Args:
            output_path: Path to save the report
            format: Report format
        """
        content = self.generate_report(format)
        output_path.write_text(content, encoding="utf-8")
        logger.info(f"Report saved to: {output_path}")