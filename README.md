# Flask QR Code Generator

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Not%20specified-lightgrey?style=for-the-badge)](https://github.com/mihaiapostol14/FlaskQrCodeGenerator)
[![Build](https://img.shields.io/badge/Build-not%20configured-lightgrey?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/mihaiapostol14/FlaskQrCodeGenerator/actions)
[![GitHub Stars](https://img.shields.io/github/stars/mihaiapostol14/FlaskQrCodeGenerator?style=for-the-badge&logo=github)](https://github.com/mihaiapostol14/FlaskQrCodeGenerator/stargazers)

**A focused Flask application for generating customizable QR-code images and persisting their metadata in MySQL.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture--tech-stack) • [Code Review](#-code-quality--security-review)

</div>


## 📸 Preview

<div align="center">

![FlaskQrCodeGenerator Preview](https://github.com/mihaiapostol14/FlaskQrCodeGenerator/blob/cbe4855e722391ee8e7e604a5faf5ebc8e32dcf5/assets/preview.png)

</div>

---

## ✨ Features

- 🧾 Generate QR codes from user-provided text or URLs.
- 🎨 Customize module size, border width, foreground color, and background color.
- 🖼️ Render generated PNG files from the application’s static asset directory.
- 💾 Persist QR-code metadata and generated image paths with SQLAlchemy.
- 🗄️ Provision a MySQL database and initialize application tables with `init_database.py`.
- ⚙️ Load database configuration from environment variables using `python-dotenv`.
- 🧩 Keep request handling, persistence, and configuration separated across small Python modules.

## 📋 Prerequisites

- Python 3.8 or higher ([Download Python](https://www.python.org/downloads/))
- pip (Python package manager, included with Python)
- Git ([Download Git](https://git-scm.com/))
- MySQL server and a user permitted to create the application database
- `venv` or another Python virtual-environment tool ([Python venv docs](https://docs.python.org/3/library/venv.html))

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/mihaiapostol14/FlaskQrCodeGenerator.git
cd FlaskQrCodeGenerator
```

### 2. Create and activate a virtual environment

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure the database

Copy the example configuration to the repository root. `python-dotenv` is loaded from the current working directory when the application starts.

```bash
cp config/.env.example .env
```

Edit `.env` with a real MySQL connection string:

```dotenv
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost:3306/qr_codes
```

Do not commit `.env` or place production credentials in source control.

### 5. Initialize the database and run the application

```bash
python init_database.py
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

> **Development warning:** `app.py` currently starts Flask with `debug=True`. Do not use this development server or debug mode in production.

## 🎮 Usage

1. Enter text or a URL in the generator form.
2. Choose the QR-code box size, border, foreground color, and background color.
3. Submit the form to generate a PNG image.
4. Use the returned QR-code view to inspect the generated image.

## 📂 Project Structure

```text
FlaskQrCodeGenerator/
├── app.py                    # Flask application factory/configuration entry point
├── views.py                  # HTTP handlers for the QR generator endpoint
├── models.py                 # SQLAlchemy model and QR image generation logic
├── init_database.py          # MySQL database provisioning and table initialization
├── requirements.txt          # Pinned Python dependencies
├── config/
│   ├── __init__.py           # Configuration package exports
│   ├── load.py               # Environment-variable loading
│   └── .env.example          # Safe configuration template
├── static/
│   └── qr_codes/             # Runtime-generated PNG files
├── templates/                # Flask/Jinja templates (required by the view)
│   └── generator.html
└── README.md
```

`static/qr_codes/` and `templates/generator.html` are runtime/application assets expected by the current code path; keep generated images out of version control unless they are intentionally used as fixtures.

## 🏗️ Architecture & Tech Stack

The application uses a small MVC-style Flask layout:

| Layer | Technology | Responsibility |
|---|---|---|
| Web layer | Flask 3.1 / `MethodView` | Routes GET and POST requests for the generator UI |
| Presentation | Jinja2 templates | Renders the generator form and generated QR code |
| Domain/persistence | Flask-SQLAlchemy / SQLAlchemy 2 | Maps `QRCodeModel` to the `qr_codes` table |
| QR generation | `qrcode` / Pillow | Builds and serializes customized PNG QR codes |
| Database | MySQL via PyMySQL | Stores content, styling settings, timestamps, and image paths |
| Configuration | `python-dotenv` | Loads `SQLALCHEMY_DATABASE_URI` from the environment |

Request flow:

```text
Browser
  │
  ▼
Flask route (views.py)
  │  validate form values and create model
  ▼
QRCodeModel (models.py)
  ├── SQLAlchemy → MySQL
  └── qrcode + Pillow → static/qr_codes/*.png
  │
  ▼
Redirect to /?qr_code=<id> → Jinja2 response
```

## 🔍 Code Quality & Security Review

### Strengths

- SQLAlchemy parameterizes normal model queries, reducing SQL-injection risk in the request path.
- Credentials are intended to be supplied through environment variables rather than hard-coded.
- Uploaded content is not treated as a file path; generated filenames are timestamp-based and server-created.
- `SQLALCHEMY_TRACK_MODIFICATIONS` is disabled, avoiding unnecessary change tracking overhead.
- The code is generally readable and uses conventional Python naming and import formatting.

### Recommended improvements before production

- **Disable debug mode:** replace `app.run(debug=True)` with environment-controlled configuration and use a production WSGI server.
- **Validate all user input:** constrain `content` to the database’s 255-character limit; bound `box_size` and `border`; and strictly validate color values as approved hex colors or named colors.
- **Add CSRF protection and rate limiting:** the state-changing POST endpoint currently has no CSRF token or abuse protection.
- **Handle transactions safely:** wrap database writes and image generation in error handling with rollback/cleanup so a failed image write cannot leave inconsistent records.
- **Avoid SQL string interpolation in provisioning:** `init_database.py` interpolates `db_name` into `CREATE DATABASE`; validate it against a strict identifier allowlist before execution.
- **Use safe database URI handling:** fail fast with a clear configuration error when `SQLALCHEMY_DATABASE_URI` is missing, and URL-encode credentials when required.
- **Manage generated files:** configure a dedicated storage backend or cleanup policy and prevent unbounded growth of `static/qr_codes`.
- **Improve ORM compatibility:** replace legacy `QRCodeModel.query.get(...)` with `db.session.get(QRCodeModel, qr_code_id)` and validate that the ID is an integer.
- **Add automated checks:** introduce tests for form validation, QR generation, database rollback, and the database initializer; add Black, Ruff/Flake8, and CI checks.
- **Improve PEP 8 consistency:** add module/class/function docstrings, type hints, constants for defaults, and consistent line wrapping. `models.py` also contains an unused `os`-adjacent design concern only insofar as file handling should be centralized and tested.
- **Define a license:** the repository currently does not include a license file; add one before accepting external contributions.

## 🧪 Development Checks

The repository does not currently include a test suite or GitHub Actions workflow. After adding development tooling, a typical local check could be:

```bash
python -m compileall .
python -m pip install black ruff pytest
ruff check .
black --check .
pytest
```

## 🤝 Contributing

1. Fork the repository.
2. Create a focused branch: `git checkout -b feat/your-change`.
3. Add tests for behavior changes.
4. Run formatting, linting, and tests locally.
5. Open a pull request with a concise description of the change and its operational impact.


## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Mihai Apostol** · [@mihaiapostol14](https://github.com/mihaiapostol14)

---

<div align="center">

**Built with Flask and Python.**

</div>
