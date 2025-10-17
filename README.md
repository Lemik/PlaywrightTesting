# Playwright UI Testing Project

This project contains UI tests using Playwright for Python.

## 🚀 Features

- Cross-browser testing support (Chromium, Firefox, WebKit)
- Headless and headed mode execution
- Flexible test selection and filtering
- Detailed test reporting
- Modern and maintainable test structure
- Comprehensive property and tenant page testing (landlord's view)
- Dedicated test runners for specific functionality

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

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
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

### Dedicated Test Runners

#### Property Tests
```bash
# Run property functionality tests
python run_property_tests.py

# Run with verbose output
python run_property_tests.py --verbose

# Run in headed mode
python run_property_tests.py --headed
```

#### Tenant Tests (Landlord's View)
```bash
# Run tenant functionality tests (landlord's view of tenants)
python run_tenant_tests.py

# Run with verbose output
python run_tenant_tests.py --verbose

# Run in headed mode
python run_tenant_tests.py --headed
```

### Advanced Test Execution

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest tests/test_example.py` | Run a specific test file |
| `pytest tests/test_example.py::test_homepage_title` | Run a specific test function |
| `pytest --headed` | Run tests with UI |
| `pytest -k "homepage"` | Run tests matching a pattern |
| `pytest -k "tenant"` | Run only tenant-related tests |
| `pytest -k "property"` | Run only property-related tests |
| `pytest -v` | Run with verbose output |
| `pytest --html=report.html` | Generate HTML test report |
| `PWDEBUG=1 pytest tests/test_admin_login.py` | Debug |
| `pytest tests/test_admin_login.py -v --log-cli-level=DEBUG` | Run with debug logging |

## 📁 Project Structure

```
PlaywrightTesting/
├── tests/                    # Test files directory
│   ├── test_admin_login.py   # Admin login tests
│   ├── test_landlord_login.py # Landlord login tests
│   ├── test_tenant_login.py  # Tenant login tests
│   ├── test_property_functionality.py # Property page tests
│   ├── test_tenant_functionality.py   # Tenant page tests (landlord's view)
│   └── conftest.py           # Test configuration
├── pom/                      # Page Object Models
│   ├── admin_page.py         # Admin page interactions
│   ├── landlord_page.py      # Landlord page interactions
│   └── tenant_page.py        # Tenant page interactions
├── helpers/                  # Helper utilities
├── reports/                  # Test reports
├── run_property_tests.py     # Property test runner
├── run_tenant_tests.py       # Tenant test runner (landlord's view)
├── PROPERTY_TESTS_README.md  # Property tests documentation
├── TENANT_TESTS_README.md    # Tenant tests documentation (landlord's view)
├── .venv/                    # Virtual environment
├── requirements.txt          # Project dependencies
└── README.md                # Project documentation
```

## 🧪 Test Coverage

### Property Tests
- Property list display and navigation
- Property details and information tabs
- Property page responsiveness
- Error handling and unauthorized access

### Tenant Tests (Landlord's View)
- Tenant list display and navigation (landlord viewing all tenants)
- Tenant details and information tabs
- Search and filter functionality
- Add new tenant functionality
- Tenant page responsiveness
- Error handling and unauthorized access

### Authentication Tests
- Admin login functionality
- Landlord login functionality
- Tenant login functionality
- Page access after authentication

## 🔧 Configuration

The project uses `pytest.ini` for test configuration. Key settings include:
- Browser selection
- Test timeout
- Screenshot capture on failure
- Video recording options

## 📚 Documentation

- [Property Tests Guide](PROPERTY_TESTS_README.md) - Comprehensive guide for property page testing
- [Tenant Tests Guide](TENANT_TESTS_README.md) - Comprehensive guide for tenant page testing (landlord's view)

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

## 🔐 Environment Variables

Create a `.env` file with the following credentials:

```env
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
``` 
