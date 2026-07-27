# {{ project_name }} API

<p align="center">
  <strong>{{ project_description }}</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-api-endpoints">API Endpoints</a> •
  <a href="#-development">Development</a> •
  <a href="#-deployment">Deployment</a>
</p>

---

## 🚀 Features

- **⚡ Fast Development** - Hot reload with `tite dev`
- **🔧 Framework Agnostic** - Supports FastAPI and Flask
- **📦 Production Ready** - Optimized for deployment
- **🔒 Secure** - Best practices built-in (CORS, rate limiting)
- **📚 OpenAPI Documentation** - Auto-generated API docs
- **🧪 Test Coverage** - Comprehensive test suite
- **🐳 Docker Ready** - Includes Dockerfile

## 📦 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd {{ project_name }}

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[fastapi]"  # For FastAPI
# OR
pip install -e ".[flask]"    # For Flask


Running the API
bash
# Start development server
tite dev

# Or run directly
python src/main.py
The API will be available at: http://localhost:8000

📚 API Documentation: http://localhost:8000/api/v1/docs

📁 Project Structure
text
{{ project_name }}/
├── src/
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── routes/              # API routes
│   │   └── health.py        # Health check endpoints
│   ├── services/            # Business logic
│   │   └── example_service.py
│   ├── models/              # Data models
│   │   └── example.py
│   └── utils/               # Utilities
│       └── helpers.py
├── tests/
│   └── test_api.py          # API tests
├── README.md
├── pyproject.toml
├── .env.example
├── Dockerfile
├── .gitignore
└── tite.toml
🔧 Configuration
Environment Variables
Create a .env file from .env.example:

bash
cp .env.example .env
Variable	Description	Default
DEBUG	Enable debug mode	false
HOST	Server host	127.0.0.1
PORT	Server port	8000
SECRET_KEY	Session secret	change-me
API_PREFIX	API URL prefix	/api/v1
LOG_LEVEL	Logging level	INFO
DATABASE_URL	Database connection	sqlite:///app.db
RATE_LIMIT	Rate limit string	100/hour
JWT_SECRET	JWT secret key	change-me
📚 API Endpoints
Health Check
Method	Endpoint	Description
GET	/api/v1/health	Health check
GET	/api/v1/health/live	Liveness probe
GET	/api/v1/health/ready	Readiness probe
GET	/api/v1/ping	Ping endpoint
🧪 Testing
bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_api.py -v
🐳 Docker Deployment
Build and Run
bash
# Build Docker image
docker build -t {{ project_name }}-api .

# Run container
docker run -p 8000:8000 {{ project_name }}-api
🚀 Deployment
Using Gunicorn (Linux/macOS)
bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
Using uvicorn
bash
pip install uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000
Production Considerations
Set DEBUG=false in production

Use a proper secret key

Configure CORS appropriately

Set up proper logging

Use a production database

Enable rate limiting

Set up monitoring

📚 API Documentation
When using FastAPI, interactive API documentation is available at:

Swagger UI: http://localhost:8000/api/v1/docs

ReDoc: http://localhost:8000/api/v1/redoc

🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Made with ❤️ using Tite