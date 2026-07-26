"""
Automation packages definition.

This module defines the default packages for Automation projects.
"""

from typing import Dict, List

# Core automation packages
AUTOMATION_PACKAGES: List[str] = [
    # Task Scheduling
    "apscheduler>=3.10.0",
    "schedule>=1.2.0",
    "celery>=5.3.0",
    "redis>=5.0.0",
    
    # Configuration
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0.0",
    "tomli>=2.0.0",
    
    # HTTP/API
    "requests>=2.31.0",
    "httpx>=0.25.0",
    "aiohttp>=3.9.0",
    "websocket-client>=1.6.0",
    
    # Web Scraping
    "beautifulsoup4>=4.12.0",
    "lxml>=4.9.0",
    "selenium>=4.15.0",
    "scrapy>=2.11.0",
    "playwright>=1.40.0",
    
    # Data Processing
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "openpyxl>=3.1.0",
    "xlrd>=2.0.0",
    "xlsxwriter>=3.1.0",
    "tabulate>=0.9.0",
    
    # File Operations
    "watchdog>=3.0.0",
    "pathspec>=0.11.0",
    "send2trash>=1.8.0",
    "python-magic>=0.4.0",
    
    # Email
    "smtplib>=0.0.0",
    "email-validator>=2.0.0",
    "yagmail>=0.15.0",
    "sendgrid>=6.10.0",
    
    # Messaging
    "python-telegram-bot>=20.0.0",
    "slack-sdk>=3.26.0",
    "discord.py>=2.3.0",
    "twilio>=8.10.0",
    
    # Database
    "sqlalchemy>=2.0.0",
    "sqlalchemy-utils>=0.41.0",
    "alembic>=1.12.0",
    "psycopg2-binary>=2.9.0; platform_system != 'Windows'",
    "psycopg2>=2.9.0; platform_system == 'Windows'",
    "sqlite3>=0.0.0",
    "aiosqlite>=0.19.0",
    
    # SSH/Remote
    "paramiko>=3.0.0",
    "cryptography>=41.0.0",
    "pywinrm>=0.4.0; platform_system == 'Windows'",
    
    # Cloud Services
    "boto3>=1.28.0",
    "google-cloud-storage>=2.10.0",
    "azure-storage-blob>=12.18.0",
    "azure-identity>=1.15.0",
    
    # CLI
    "click>=8.0.0",
    "typer>=0.9.0",
    "argparse>=1.4.0",
    "rich>=13.0.0",
    "prompt-toolkit>=3.0.0",
    "questionary>=2.0.0",
    
    # Logging
    "loguru>=0.7.0",
    "colorlog>=6.7.0",
    "structlog>=23.0.0",
    
    # Monitoring
    "prometheus-client>=0.19.0",
    "statsd>=4.0.0",
    "datadog>=0.46.0",
    
    # Testing
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-xdist>=3.3.0",
    "pytest-mock>=3.11.0",
    "pytest-timeout>=2.1.0",
    "pytest-html>=3.2.0",
    
    # Code Quality
    "black>=22.0.0",
    "isort>=5.10.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0.0",
]

# Essential packages (always included)
ESSENTIAL_PACKAGES: List[str] = [
    "apscheduler>=3.10.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "click>=8.0.0",
    "rich>=13.0.0",
    "loguru>=0.7.0",
    "requests>=2.31.0",
]

# Optional packages (select based on needs)
OPTIONAL_PACKAGES: Dict[str, List[str]] = {
    "web_scraping": [
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "selenium>=4.15.0",
        "scrapy>=2.11.0",
    ],
    "messaging": [
        "python-telegram-bot>=20.0.0",
        "slack-sdk>=3.26.0",
        "discord.py>=2.3.0",
    ],
    "cloud": [
        "boto3>=1.28.0",
        "google-cloud-storage>=2.10.0",
        "azure-storage-blob>=12.18.0",
    ],
    "remote": [
        "paramiko>=3.0.0",
        "cryptography>=41.0.0",
    ],
    "data": [
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
    ],
}