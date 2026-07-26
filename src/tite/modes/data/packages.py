"""
Data Science packages definition.

This module defines the default packages for Data Science projects.
"""

from typing import List

# Core data science packages
DATA_PACKAGES: List[str] = [
    # Data manipulation
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "polars>=0.19.0",
    "dask>=2023.10.0",
    "xarray>=2023.10.0",
    
    # Visualization
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    "plotly>=5.14.0",
    "bokeh>=3.0.0",
    "altair>=5.0.0",
    "ggplot>=0.11.0",
    "streamlit>=1.25.0",
    
    # Machine Learning
    "scikit-learn>=1.2.0",
    "scipy>=1.10.0",
    "statsmodels>=0.14.0",
    "xgboost>=1.7.0",
    "lightgbm>=4.0.0",
    "catboost>=1.2.0",
    "imbalanced-learn>=0.10.0",
    
    # Deep Learning
    "tensorflow>=2.13.0",
    "torch>=2.0.0",
    "torchvision>=0.15.0",
    "keras>=2.13.0",
    
    # Feature Engineering
    "feature-engine>=1.5.0",
    "category-encoders>=2.6.0",
    
    # Model Evaluation
    "yellowbrick>=1.5.0",
    "scikit-plot>=0.3.0",
    
    # Hyperparameter Tuning
    "optuna>=3.3.0",
    "hyperopt>=0.2.0",
    "scikit-optimize>=0.9.0",
    "ray[tune]>=2.7.0",
    
    # Data Version Control
    "dvc>=3.0.0",
    "dagshub>=0.2.0",
    
    # Experiment Tracking
    "mlflow>=2.6.0",
    "wandb>=0.15.0",
    
    # Database Integration
    "sqlalchemy>=2.0.0",
    "sqlalchemy-utils>=0.41.0",
    "alembic>=1.12.0",
    "psycopg2-binary>=2.9.0; platform_system != 'Windows'",
    "psycopg2>=2.9.0; platform_system == 'Windows'",
    "sqlite3>=0.0.0",
    
    # Big Data
    "pyspark>=3.4.0",
    "dask[complete]>=2023.10.0",
    
    # Cloud Storage
    "s3fs>=2023.10.0",
    "gcsfs>=2023.10.0",
    "azure-storage-blob>=12.18.0",
    
    # API Integration
    "requests>=2.31.0",
    "httpx>=0.25.0",
    "aiohttp>=3.9.0",
    
    # Configuration
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    
    # Notebook Support
    "jupyter>=1.0.0",
    "notebook>=7.0.0",
    "ipykernel>=6.0.0",
    "ipywidgets>=8.0.0",
    "jupyterlab>=4.0.0",
    "nbconvert>=7.0.0",
    "papermill>=2.4.0",
    
    # Reporting
    "nbformat>=5.9.0",
    "markdown>=3.5.0",
    "jinja2>=3.0.0",
    "weasyprint>=60.0.0",
    
    # Logging
    "loguru>=0.7.0",
    "rich>=13.0.0",
    "tqdm>=4.66.0",
    
    # Testing
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-xdist>=3.3.0",
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
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "matplotlib>=3.7.0",
    "jupyter>=1.0.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "click>=8.0.0",
    "rich>=13.0.0",
]

# Optional packages (select based on needs)
OPTIONAL_PACKAGES: Dict[str, List[str]] = {
    "deep_learning": [
        "tensorflow>=2.13.0",
        "torch>=2.0.0",
        "keras>=2.13.0",
    ],
    "big_data": [
        "pyspark>=3.4.0",
        "dask[complete]>=2023.10.0",
    ],
    "cloud": [
        "s3fs>=2023.10.0",
        "gcsfs>=2023.10.0",
        "azure-storage-blob>=12.18.0",
    ],
    "experiment_tracking": [
        "mlflow>=2.6.0",
        "wandb>=0.15.0",
    ],
    "dashboard": [
        "streamlit>=1.25.0",
        "dash>=2.14.0",
    ],
    "gpu": [
        "cupy-cuda11x>=12.0.0",
        "jax>=0.4.0",
    ],
}