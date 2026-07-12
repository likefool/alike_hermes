# Project Alpha: NoteVault

A lightweight, secure,-RESTful Note-taking application built with Python (Flask) and a single-page HTML/JS frontend. This project demonstrates a decoupled architecture with isolated environment management using `uv`.

## 🛠 Tech Stack
- **Backend:** Python 3.11+, Flask, SQLite3
- **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla)
- **Environment Management:** `uv` (Fast Python package installer and resolver)

---

## 🚀 Quick Start (Development Workflow)

This project uses a dedicated directory structure to manage multiple sandboxes. Follow these steps to set up your environment.

### 1. Prerequisites
Ensure you have [uv](https://github.com/astral-sh/uv) installed on your host machine.

### 2. Setup Development Environment
Create a development sandbox including all linting and testing tools.

```bash
# Create the dev environment
uv venv projects/project_alpha/environments/dev

# Install dependencies and the project in editable mode
projects/project_alpha/environments/dev/bin/python -m pip install -e projects/project_alpha/
```

### 3. Running the Application
Start the Flask server using the development environment:

```bash
projects/project_alpha/environments/dev/bin/python projects/project_alpha/src/notes_api.py
```

### 4. Accessing the UI
Once the server is running, open the following file in your web browser:
`projects/project_alpha/src/index.html`

---

## 🧪 Testing & Quality Assurance

### Running Tests
To ensure the integrity of the code, run the test suite in the isolated testing environment:

```bash
# Create test environment
uv venv projects/project_alpha/environments/test
uv pip install -e projects/project_alpha/

# Run tests
projects/project_alpha/environments/test/bin/python -m pytest
```

### Linting & Formatting
To maintain code quality, use `ruff` (installed in dev env):

```bash
projects/project_alpha/environments/dev/bin/python -m ruff check .
projects/project_alpha/environments/dev/bin/python -m ruff format .
```

---

## 📁 Directory Structure Overview

- `projects/project_alpha/`
    - `pyproject.toml`: The single source of truth for dependencies.
    - `src/`: The source code (`notes_api.py`, `index.html`).
    - `environments/`: Isolated sandboxes (dev, test, prod).
- `projects/project_alpha/src/notes_api.py`: The RESTful API.
- `projects/project_alpha/src/index.html`: The Single Page Application (SPA) frontend.

## 🔐 Security Note
This project was designed with security-first principles, including:
- **Parameterized SQL Queries** to prevent SQL Injection.
- **XSS-protected UI** using DOM-based rendering.
- **Environment Isolation** via `uv` to prevent dependency leakage.
