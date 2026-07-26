"""
AI/ML packages definition.

This module defines the default packages for AI/ML projects.
"""

from typing import Dict, List

# Core AI/ML packages
AI_PACKAGES: List[str] = [
    # LLM Providers
    "openai>=1.0.0",
    "anthropic>=0.18.0",
    "cohere>=4.0.0",
    "google-generativeai>=0.3.0",
    
    # LangChain Ecosystem
    "langchain>=0.3.0",
    "langchain-core>=0.3.0",
    "langchain-community>=0.3.0",
    "langchain-openai>=0.1.0",
    "langchain-anthropic>=0.1.0",
    "langchain-cohere>=0.1.0",
    "langchain-google-genai>=0.1.0",
    "langgraph>=0.0.20",
    
    # Deep Learning Frameworks
    "torch>=2.0.0",
    "torchvision>=0.15.0",
    "torchaudio>=2.0.0",
    "tensorflow>=2.13.0",
    "tensorflow-hub>=0.14.0",
    "tensorflow-text>=2.13.0",
    
    # Transformers & Models
    "transformers>=4.30.0",
    "sentence-transformers>=2.2.0",
    "huggingface-hub>=0.16.0",
    "tokenizers>=0.13.0",
    "accelerate>=0.24.0",
    "bitsandbytes>=0.41.0",
    "peft>=0.6.0",
    "trl>=0.7.0",
    "datasets>=2.14.0",
    "evaluate>=0.4.0",
    
    # Vector Databases
    "chromadb>=0.4.0",
    "faiss-cpu>=1.7.4",
    "pinecone-client>=2.2.0",
    "weaviate-client>=3.22.0",
    "qdrant-client>=1.7.0",
    "pgvector>=0.2.0",
    "redis>=5.0.0",
    
    # RAG & Retrieval
    "ragatouille>=0.2.0",
    "unstructured>=0.10.0",
    "pdf2image>=1.16.0",
    "pypdf>=3.16.0",
    "docx2txt>=0.8",
    "markdown>=3.5.0",
    "beautifulsoup4>=4.12.0",
    
    # Embeddings
    "sentencepiece>=0.1.99",
    "tiktoken>=0.5.0",
    "optimum>=1.12.0",
    "onnxruntime>=1.15.0",
    
    # Fine-tuning
    "pytorch-lightning>=2.0.0",
    "transformers[torch]>=4.30.0",
    "datasets>=2.14.0",
    "peft>=0.6.0",
    "trl>=0.7.0",
    "unsloth>=2023.12.0",
    
    # Evaluation
    "evaluate>=0.4.0",
    "scikit-learn>=1.2.0",
    "scipy>=1.10.0",
    "rouge-score>=0.1.2",
    "bert-score>=0.3.13",
    "sacrebleu>=2.3.0",
    
    # Configuration
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0.0",
    
    # Utilities
    "click>=8.0.0",
    "rich>=13.0.0",
    "tqdm>=4.66.0",
    "loguru>=0.7.0",
    "joblib>=1.3.0",
    "cachetools>=5.3.0",
    
    # Web/API
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "requests>=2.31.0",
    "httpx>=0.25.0",
    "aiohttp>=3.9.0",
    "websockets>=12.0",
    
    # Monitoring
    "prometheus-client>=0.19.0",
    "opentelemetry-api>=1.20.0",
    "opentelemetry-sdk>=1.20.0",
    "opentelemetry-exporter-otlp>=1.20.0",
    
    # Testing
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-xdist>=3.3.0",
    "pytest-mock>=3.11.0",
    
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
    "openai>=1.0.0",
    "langchain>=0.3.0",
    "langchain-openai>=0.1.0",
    "transformers>=4.30.0",
    "torch>=2.0.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "click>=8.0.0",
    "rich>=13.0.0",
    "loguru>=0.7.0",
    "tqdm>=4.66.0",
    "chromadb>=0.4.0",
    "tiktoken>=0.5.0",
]

# Optional packages (select based on needs)
OPTIONAL_PACKAGES: Dict[str, List[str]] = {
    "vision": [
        "torchvision>=0.15.0",
        "transformers[vision]>=4.30.0",
        "pillow>=10.0.0",
        "opencv-python>=4.8.0",
        "detectron2>=0.6.0",
        "segment-anything>=1.0.0",
    ],
    "speech": [
        "torchaudio>=2.0.0",
        "whisper>=1.1.10",
        "soundfile>=0.12.0",
        "librosa>=0.10.0",
        "speechbrain>=0.5.14",
    ],
    "fine_tuning": [
        "peft>=0.6.0",
        "trl>=0.7.0",
        "unsloth>=2023.12.0",
        "pytorch-lightning>=2.0.0",
        "accelerate>=0.24.0",
        "bitsandbytes>=0.41.0",
    ],
    "vector_db": [
        "faiss-cpu>=1.7.4",
        "pinecone-client>=2.2.0",
        "weaviate-client>=3.22.0",
        "qdrant-client>=1.7.0",
        "pgvector>=0.2.0",
    ],
    "langchain_extras": [
        "langchain-community>=0.3.0",
        "langchain-anthropic>=0.1.0",
        "langchain-cohere>=0.1.0",
        "langchain-google-genai>=0.1.0",
        "langgraph>=0.0.20",
    ],
    "evaluation": [
        "evaluate>=0.4.0",
        "rouge-score>=0.1.2",
        "bert-score>=0.3.13",
        "sacrebleu>=2.3.0",
    ],
    "api": [
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "websockets>=12.0",
    ],
    "monitoring": [
        "prometheus-client>=0.19.0",
        "opentelemetry-api>=1.20.0",
        "opentelemetry-sdk>=1.20.0",
    ],
}