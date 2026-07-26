# Tite

<p align="center">
  <img src="https://raw.githubusercontent.com/aldanedev-create/TITE/main/assets/tite.png" alt="Tite Logo"
   width="200"/>
   <sub>Start Coding right now!!</sub>
</p>

<h1 align="center">Zero-Configuration Python Project Bootstrapper</h1>

<p align="center">
  <strong>Python project setup in seconds. Framework-independent. Production-ready.</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-modes">Modes</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## GETTING STARTING
CHECK WEBSITE LINK :  <a href="https://tite-public-website.vercel.app/getting-started">Click me</a> •



## 🚀 Features

- **⚡ Zero Configuration** - Start coding immediately, no setup files needed
- **📁 Standardized Structure** - Consistent project organization every time
- **🔧 Framework Agnostic** - Works with Flask, FastAPI, Django, PySide, AI/ML, and more
- **🐍 Virtual Environment** - Automatically creates and manages `.venv`
- **📦 Git Integration** - Initializes repository with proper `.gitignore`
- **📄 Project Files** - Generates `README.md`, `pyproject.toml`, and more
- **🔄 Hot Reload** - Development server with file watching (like Vite for Python)
- **🏥 Health Checks** - `tite doctor` validates your project setup
- **🧹 Clean Commands** - Remove cache and build artifacts
- **🎯 Mode System** - Domain-specific presets for Data Science, AI, Automation

## 📦 Installation

```bash
# Install from PyPI 
pip install tite-sc

# Or install from source
git clone https://github.com/aldanedev-create/TITE.git
cd tite
pip install -e .


🎯 Quick Start
bash
# Create a new project
tite new my-awesome-project

# Enter the project directory
cd my-awesome-project

# Start development with hot reload
tite dev

# Check project health
tite doctor
📚 Commands
Command	Description
tite new <name>	Create a new Python project
tite dev	Start development server with hot reload
tite doctor	Run health checks on the project
tite clean	Remove cache and build artifacts
tite info	Display project information
tite config	View or modify configuration
tite env	Show environment details
tite mode <mode> <name>	Create project with domain-specific preset

🎨 Modes
Tite provides pre-configured project setups for common development domains:

Data Science
bash
tite mode data sales-analysis
Creates a project with:

Data directories (data/raw/, data/processed/)

Jupyter notebooks folder

Pandas, NumPy, Matplotlib pre-configured

AI / Machine Learning
bash
tite mode ai chatbot-assistant
Creates a project with:

Prompts directory

Models folder

OpenAI, LangChain, Transformers ready

Automation
bash
tite mode automation backup-tool
Creates a project with:

Tasks directory

Logging configuration

Environment variables support

🏗️ Project Structure
text
my-project/
├── .venv/              # Virtual environment
├── src/                # Source code
│   └── main.py
├── tests/              # Test files
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
└── pyproject.toml      # Project configuration

💡 Examples

Web API with FastAPI
bash
tite new banking-api
cd banking-api
pip install fastapi uvicorn
echo "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef home():\n    return {'message': 'Bank API'}" > src/main.py
tite dev
AI Assistant
bash
tite mode ai assistant
cd assistant
pip install openai langchain
# Write your AI code in src/main.py
tite dev
Data Analysis
bash
tite mode data customer-analysis
cd customer-analysis
# Start working in notebooks/ or src/
tite dev

🧪 Development
bash
# Clone the repository
git clone https://github.com/aldanedev-create/TITE.git
cd tite

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black src/
isort src/
flake8 src/
mypy src/

🤝 Contributing
We welcome contributions! Please see our Contributing Guide for details.

Quick Contribution Steps
Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Inspired by Vite for JavaScript

Built for the Python community

Made with ❤️ for Python developers everywhere 