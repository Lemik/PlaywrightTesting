# Playwright UI Testing Project

This project contains UI tests using Playwright for Python.

## 🚀 Features

- Cross-browser testing support (Chromium, Firefox, WebKit)
- Headless and headed mode execution
- Flexible test selection and filtering
- Detailed test reporting
- Modern and maintainable test structure

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (for version control)

## 🛠️ Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd PlaywrightTesting
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## 🌐 Virtual Environment Management

### Activating the Virtual Environment

- On macOS/Linux:
```bash
source .venv/bin/activate
```
- On Windows:
```bash
.venv\Scripts\activate
```

### Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment:
```bash
deactivate
```

### Managing Dependencies

- To install a new package:
```bash
pip install package_name
```

- To save current dependencies to requirements.txt:
```bash
pip freeze > requirements.txt
```

- To install from requirements.txt:
```bash
pip install -r requirements.txt
```

### Best Practices

- Always activate the virtual environment before working on the project
- Keep requirements.txt updated when adding new dependencies
- Never commit the .venv directory to version control (it's already in .gitignore)
- Use `python -m pip` instead of just `pip` to ensure you're using the correct pip

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run tests with UI (headed mode)
pytest --headed

# Run tests in a specific browser
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Advanced Test Execution

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest tests/test_example.py` | Run a specific test file |
| `pytest tests/test_example.py::test_homepage_title` | Run a specific test function |
| `pytest --headed` | Run tests with UI |
| `pytest -k "homepage"` | Run tests matching a pattern |
| `pytest -v` | Run with verbose output |
| `pytest --html=report.html` | Generate HTML test report |
| `PWDEBUG=1 pytest tests/test_admin_login.py` | Debug |
| `pytest tests/test_admin_login.py -v --log-cli-level=DEBUG` | Run with debug logging |

## 📁 Project Structure

```
PlaywrightTesting/
├── tests/               # Test files directory
├── .venv/              # Virtual environment
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## 🔧 Configuration

The project uses `pytest.ini` for test configuration. Key settings include:
- Browser selection
- Test timeout
- Screenshot capture on failure
- Video recording options

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For any questions or suggestions, please open an issue in the repository. 

# Admin credentials
ADMIN_USER_EMAIL=admin@example.com
ADMIN_USER_PASSWORD=admin_password

# Landlord credentials
LANDLORD_USER_EMAIL=landlord@example.com
LANDLORD_USER_PASSWORD=landlord_password

# Tenant credentials
TenantA_USER_EMAIL=tenantA@example.com
TenantA_USER_PASSWORD=tenantA_password

TenantB_USER_EMAIL=tenantB@example.com
TenantB_USER_PASSWORD=tenantB_password

# Base URL for the application
URL=http://localhost:3000 
