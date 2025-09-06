@echo off
echo ========================================
echo 🚀 Luminis AI Library - CI Test Script
echo ========================================
echo.

echo 📋 Step 1: Installing dependencies...
pip install -r requirements.txt
pip install bandit safety flake8 black pytest pytest-cov
echo.

echo 🔒 Step 2: Security checks...
echo Running Bandit...
bandit -r . -f json -o bandit-report.json
echo Running Safety...
safety check --json > safety-report.json
echo.

echo 🎨 Step 3: Code quality checks...
echo Running Flake8...
flake8 .
if %errorlevel% neq 0 (
    echo ❌ Flake8 found issues!
    exit /b 1
)
echo Running Black check...
black --check .
if %errorlevel% neq 0 (
    echo ❌ Black found formatting issues!
    echo 💡 Run 'black .' to fix formatting
    exit /b 1
)
echo.

echo 🧪 Step 4: Running tests...
set PYTHONPATH=%PYTHONPATH%;%cd%\src
pytest --maxfail=1 --disable-warnings -q
if %errorlevel% neq 0 (
    echo ❌ Tests failed!
    exit /b 1
)
echo.

echo 📊 Step 5: Coverage report...
pytest --cov=src/backend --cov-report=xml:coverage.xml
echo.

echo ✅ All CI checks passed! Ready for GitHub Actions.
echo.
echo 📁 Generated reports:
echo   - bandit-report.json
echo   - safety-report.json  
echo   - coverage.xml
echo.
pause
