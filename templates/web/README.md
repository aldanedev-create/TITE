# {{ project_name }}

<p align="center">
  <strong>{{ project_description }}</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-development">Development</a> •
  <a href="#-deployment">Deployment</a>
</p>

---

## 🚀 Features

- **⚡ Fast Development** - Hot reload with `tite dev`
- **🔧 Framework Agnostic** - Supports FastAPI, Flask, or Django
- **📦 Production Ready** - Optimized for deployment
- **🎨 Modern UI** - Beautiful default template
- **📱 Responsive** - Works on all devices
- **🔒 Secure** - Best practices built-in

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
pip install -e .

# Or install with specific framework
pip install -e ".[fastapi]"  # For FastAPI
pip install -e ".[flask]"    # For Flask


Running the Application
bash
# Start development server
tite dev

# Or run directly
python src/main.py
The application will be available at: http://localhost:8000

📁 Project Structure
text
{{ project_name }}/
├── src/
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── templates/           # HTML templates
│   │   └── index.html       # Home page template
│   └── static/              # Static assets
│       ├── css/
│       │   └── style.css    # Stylesheets
│       └── js/
│           └── main.js      # JavaScript
├── tests/
│   └── test_app.py          # Application tests
├── README.md
├── pyproject.toml
├── .env.example
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
LOG_LEVEL	Logging level	INFO
DATABASE_URL	Database connection	sqlite:///app.db
Tite Configuration
tite.toml controls Tite-specific behavior:

toml
[dev]
command = "python src/main.py"
port = 8000
host = "127.0.0.1"

[watcher]
paths = ["src", "tests"]
extensions = [".py", ".html", ".css", ".js"]
🧪 Testing
bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_app.py -v
🚀 Deployment
Using Gunicorn (Linux/macOS)
bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
Using uvicorn
bash
pip install uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000
Docker Deployment
dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
📚 Framework Support
FastAPI
bash
pip install ".[fastapi]"
Flask
bash
pip install ".[flask]"
Django
bash
pip install django
# Then migrate to Django structure
🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Made with ❤️ using Tite