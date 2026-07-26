"""
Report generation for Tite.

This module provides report generation for diagnostic results
in various formats including text, JSON, markdown, and HTML.
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from tite.diagnostics.checks import CheckResult, CheckStatus


class ReportFormat(Enum):
    """Report format options."""
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"


class ReportGenerator:
    """
    Generates reports from diagnostic results.
    
    This class generates reports in various formats including
    text, JSON, markdown, and HTML.
    
    Attributes:
        format: Report format
    """
    
    def __init__(self, format: ReportFormat = ReportFormat.TEXT):
        """
        Initialize the report generator.
        
        Args:
            format: Report format
        """
        self.format = format
        
    def generate(
        self,
        results: List[CheckResult],
        project_path: Path,
    ) -> str:
        """
        Generate a report from check results.
        
        Args:
            results: List of check results
            project_path: Path to the project
            
        Returns:
            str: Report content
        """
        if self.format == ReportFormat.TEXT:
            return self._generate_text(results, project_path)
        elif self.format == ReportFormat.JSON:
            return self._generate_json(results, project_path)
        elif self.format == ReportFormat.MARKDOWN:
            return self._generate_markdown(results, project_path)
        elif self.format == ReportFormat.HTML:
            return self._generate_html(results, project_path)
        else:
            return self._generate_text(results, project_path)
            
    def _generate_text(self, results: List[CheckResult], project_path: Path) -> str:
        """Generate text report."""
        lines = []
        lines.append("=" * 60)
        lines.append(f"Tite Doctor Report")
        lines.append("=" * 60)
        lines.append(f"Project: {project_path}")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        lines.append("")
        
        total = len(results)
        passed = sum(1 for r in results if r.status == CheckStatus.PASSED)
        warnings = sum(1 for r in results if r.status == CheckStatus.WARNING)
        failed = sum(1 for r in results if r.status == CheckStatus.FAILED)
        
        lines.append(f"Summary:")
        lines.append(f"  Total checks: {total}")
        lines.append(f"  Passed: {passed}")
        lines.append(f"  Warnings: {warnings}")
        lines.append(f"  Failed: {failed}")
        
        if failed > 0:
            lines.append(f"  Status: UNHEALTHY")
        elif warnings > 0:
            lines.append(f"  Status: WARNING")
        else:
            lines.append(f"  Status: HEALTHY")
            
        lines.append("")
        lines.append("-" * 60)
        lines.append("")
        
        for result in results:
            icon = "✓" if result.status == CheckStatus.PASSED else "⚠" if result.status == CheckStatus.WARNING else "✗"
            lines.append(f"{icon} {result.check_name}")
            if result.message:
                lines.append(f"  {result.message}")
            if result.details:
                for key, value in result.details.items():
                    lines.append(f"    {key}: {value}")
            if result.recommendations:
                lines.append("  Recommendations:")
                for rec in result.recommendations:
                    lines.append(f"    - {rec}")
            lines.append("")
            
        lines.append("=" * 60)
        
        return "\n".join(lines)
        
    def _generate_json(self, results: List[CheckResult], project_path: Path) -> str:
        """Generate JSON report."""
        data = {
            "project": str(project_path),
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(results),
                "passed": sum(1 for r in results if r.status == CheckStatus.PASSED),
                "warnings": sum(1 for r in results if r.status == CheckStatus.WARNING),
                "failed": sum(1 for r in results if r.status == CheckStatus.FAILED),
            },
            "checks": [r.to_dict() for r in results],
        }
        
        return json.dumps(data, indent=2)
        
    def _generate_markdown(self, results: List[CheckResult], project_path: Path) -> str:
        """Generate markdown report."""
        lines = []
        lines.append("# Tite Doctor Report")
        lines.append("")
        lines.append(f"**Project:** `{project_path}`")
        lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        total = len(results)
        passed = sum(1 for r in results if r.status == CheckStatus.PASSED)
        warnings = sum(1 for r in results if r.status == CheckStatus.WARNING)
        failed = sum(1 for r in results if r.status == CheckStatus.FAILED)
        
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total checks:** {total}")
        lines.append(f"- **Passed:** {passed}")
        lines.append(f"- **Warnings:** {warnings}")
        lines.append(f"- **Failed:** {failed}")
        
        if failed > 0:
            lines.append(f"- **Status:** ❌ UNHEALTHY")
        elif warnings > 0:
            lines.append(f"- **Status:** ⚠️ WARNING")
        else:
            lines.append(f"- **Status:** ✅ HEALTHY")
            
        lines.append("")
        lines.append("## Check Results")
        lines.append("")
        
        for result in results:
            icon = "✅" if result.status == CheckStatus.PASSED else "⚠️" if result.status == CheckStatus.WARNING else "❌"
            lines.append(f"### {icon} {result.check_name}")
            if result.message:
                lines.append(f"**Message:** {result.message}")
            if result.details:
                lines.append("**Details:**")
                for key, value in result.details.items():
                    lines.append(f"- {key}: {value}")
            if result.recommendations:
                lines.append("**Recommendations:**")
                for rec in result.recommendations:
                    lines.append(f"- {rec}")
            lines.append("")
            
        return "\n".join(lines)
        
    def _generate_html(self, results: List[CheckResult], project_path: Path) -> str:
        """Generate HTML report."""
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("<meta charset='utf-8'>")
        html.append("<title>Tite Doctor Report</title>")
        html.append("<style>")
        html.append("""
body { font-family: Arial, sans-serif; margin: 40px; max-width: 900px; margin: 0 auto; padding: 20px; }
h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
.summary { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
.summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.summary-item { text-align: center; padding: 10px; background: white; border-radius: 5px; }
.summary-item .number { font-size: 24px; font-weight: bold; }
.summary-item .label { color: #666; font-size: 12px; }
.passed .number { color: #4CAF50; }
.warning .number { color: #FFC107; }
.failed .number { color: #f44336; }
.check { background: white; border: 1px solid #e0e0e0; border-radius: 5px; padding: 15px; margin: 10px 0; }
.check.passed { border-left: 4px solid #4CAF50; }
.check.warning { border-left: 4px solid #FFC107; }
.check.failed { border-left: 4px solid #f44336; }
.check-title { font-weight: bold; font-size: 16px; }
.check-status { font-size: 20px; margin-right: 10px; }
.details { margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 3px; }
.details-item { margin: 2px 0; }
.recommendations { margin: 10px 0; padding: 10px; background: #fff3cd; border-radius: 3px; border-left: 3px solid #ffc107; }
.recommendation { margin: 2px 0; }
.status-healthy { color: #4CAF50; }
.status-warning { color: #FFC107; }
.status-unhealthy { color: #f44336; }
""")
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        
        # Title
        html.append("<h1>🏥 Tite Doctor Report</h1>")
        html.append(f"<p><strong>Project:</strong> {project_path}</p>")
        html.append(f"<p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        # Summary
        total = len(results)
        passed = sum(1 for r in results if r.status == CheckStatus.PASSED)
        warnings = sum(1 for r in results if r.status == CheckStatus.WARNING)
        failed = sum(1 for r in results if r.status == CheckStatus.FAILED)
        
        status_text = "HEALTHY" if failed == 0 and warnings == 0 else "WARNING" if failed == 0 else "UNHEALTHY"
        status_class = "status-healthy" if status_text == "HEALTHY" else "status-warning" if status_text == "WARNING" else "status-unhealthy"
        
        html.append("<div class='summary'>")
        html.append("<div class='summary-grid'>")
        html.append(f"<div class='summary-item'><div class='number'>{total}</div><div class='label'>Total Checks</div></div>")
        html.append(f"<div class='summary-item passed'><div class='number'>{passed}</div><div class='label'>Passed</div></div>")
        html.append(f"<div class='summary-item warning'><div class='number'>{warnings}</div><div class='label'>Warnings</div></div>")
        html.append(f"<div class='summary-item failed'><div class='number'>{failed}</div><div class='label'>Failed</div></div>")
        html.append("</div>")
        html.append(f"<p><strong>Status:</strong> <span class='{status_class}'>{status_text}</span></p>")
        html.append("</div>")
        
        # Check results
        html.append("<h2>Check Results</h2>")
        
        for result in results:
            status_class = result.status.value
            icon = "✅" if result.status == CheckStatus.PASSED else "⚠️" if result.status == CheckStatus.WARNING else "❌"
            
            html.append(f"<div class='check {status_class}'>")
            html.append(f"<div class='check-title'><span class='check-status'>{icon}</span> {result.check_name}</div>")
            if result.message:
                html.append(f"<p><strong>Message:</strong> {result.message}</p>")
            if result.details:
                html.append("<div class='details'>")
                for key, value in result.details.items():
                    html.append(f"<div class='details-item'><strong>{key}:</strong> {value}</div>")
                html.append("</div>")
            if result.recommendations:
                html.append("<div class='recommendations'>")
                html.append("<strong>Recommendations:</strong>")
                for rec in result.recommendations:
                    html.append(f"<div class='recommendation'>• {rec}</div>")
                html.append("</div>")
            html.append("</div>")
            
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)