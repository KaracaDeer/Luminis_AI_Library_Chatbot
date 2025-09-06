#!/usr/bin/env python3
"""
Luminis.AI Library Assistant - Comprehensive Test Runner
========================================================

This file is the main test runner that executes all tests in the Luminis.AI
Library Assistant project. It provides a unified way to run Python tests,
Node.js tests, and perform comprehensive system validation.

What This Test Runner Does:
1. Python Tests: Executes all Python backend tests (unit, integration, backend)
2. Node.js Tests: Runs frontend tests using npm test scripts
3. Dependency Checks: Validates that all required packages are installed
4. System Validation: Performs comprehensive project health checks
5. Test Reporting: Provides detailed feedback on test execution results

Test Categories Covered:
- Basic functionality tests
- Backend service tests
- Frontend component tests
- Integration tests
- System configuration tests
- Dependency validation tests

Usage:
- Run this file to execute all tests: python tests/run_all_tests.py
- Individual test files can also be run separately
- Provides comprehensive project validation
- Essential for CI/CD pipeline integration

Benefits:
- Single command to run all tests
- Comprehensive project validation
- Early detection of integration issues
- Quality assurance automation
- Development workflow improvement

This test runner is essential for:
- Development environment validation
- Continuous integration processes
- Quality assurance workflows
- Production deployment verification
- System reliability assurance
"""

import unittest
import sys
import os
import time
import subprocess
from pathlib import Path

# Proje kök dizinini path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_python_tests():
    """Runs Python tests"""
    print("🐍 Running Python Tests...")
    print("=" * 50)

    # Find test files
    test_files = ["tests/test_basic.py", "tests/test_backend.py", "tests/test_frontend.py", "tests/test_integration.py"]

    # Run each test file separately
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📁 Testing {test_file}...")
            try:
                # Run test file
                result = subprocess.run(
                    [sys.executable, "-m", "unittest", test_file, "-v"],
                    capture_output=True,
                    text=True,
                    cwd=project_root,
                )

                if result.returncode == 0:
                    print(f"OK: {test_file} completed successfully")
                else:
                    print(f"ERROR: {test_file} completed with errors")
                    print(f"Stdout: {result.stdout}")
                    print(f"Stderr: {result.stderr}")

            except Exception as e:
                print(f"ERROR: {test_file} could not be run: {e}")
        else:
            print(f"WARNING: {test_file} not found")


def run_node_tests():
    """Runs Node.js tests"""
    print("\n🟢 Running Node.js Tests...")
    print("=" * 50)

    # Check if test script exists in frontend package.json
    frontend_dir = project_root / "src" / "frontend"
    package_json_path = frontend_dir / "package.json"

    if package_json_path.exists():
        try:
            import json

            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)

            if "scripts" in package_data and "test" in package_data["scripts"]:
                print("📦 Running npm test...")
                # Check if npm is available
                import shutil

                if shutil.which("npm"):
                    result = subprocess.run(["npm", "test"], capture_output=True, text=True, cwd=frontend_dir)

                    if result.returncode == 0:
                        print("OK: npm test completed successfully")
                    else:
                        print("ERROR: npm test completed with errors")
                        print(f"Stdout: {result.stdout}")
                        print(f"Stderr: {result.stderr}")
                else:
                    print("WARNING: npm not found - test script exists but cannot be run")
            else:
                print("WARNING: test script not found in package.json")

        except Exception as e:
            if "Sistem belirtilen dosyayı bulamıyor" in str(e) or "not found" in str(e).lower():
                print("WARNING: npm not found in PATH - test script exists but cannot be run")
            else:
                print(f"ERROR: package.json could not be tested: {e}")
    else:
        print("WARNING: Frontend package.json not found")


def check_dependencies():
    """Checks dependencies"""
    print("\n🔍 Dependency Check...")
    print("=" * 50)

    # Python dependencies
    print("🐍 Checking Python dependencies...")
    try:
        import fastapi

        print("OK: FastAPI installed")
    except ImportError:
        print("ERROR: FastAPI not installed")

    try:
        import openai

        print("OK: OpenAI installed")
    except ImportError:
        print("ERROR: OpenAI not installed")

    try:
        import sqlalchemy

        print("OK: SQLAlchemy installed")
    except ImportError:
        print("ERROR: SQLAlchemy not installed")

    # Node.js dependencies
    print("\n🟢 Checking Node.js dependencies...")
    frontend_dir = project_root / "src" / "frontend"
    node_modules_path = frontend_dir / "node_modules"
    if node_modules_path.exists():
        print("OK: Frontend node_modules found")
    else:
        print("ERROR: Frontend node_modules not found - npm install should be run")

    package_lock_path = frontend_dir / "package-lock.json"
    if package_lock_path.exists():
        print("OK: Frontend package-lock.json found")
    else:
        print("ERROR: Frontend package-lock.json not found")


def check_project_structure():
    """Checks project structure"""
    print("\n📁 Project Structure Check...")
    print("=" * 50)

    required_dirs = [
        "src",
        "src/backend",
        "src/frontend",
        "src/frontend/components",
        "src/frontend/contexts",
        "src/frontend/services",
        "src/frontend/stores",
        "src/database",
        "src/services",
        "tests",
        "docs",
    ]

    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path}")

    required_files = [
        "src/backend/main.py",
        "src/frontend/package.json",
        "src/frontend/tsconfig.json",
        "src/frontend/vite.config.ts",
        "requirements.txt",
        "docker-compose.yml",
        "README.md",
    ]

    print("\n📄 Required Files:")
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")


def run_build_tests():
    """Runs build tests"""
    print("\n🔨 Build Tests...")
    print("=" * 50)

    frontend_dir = project_root / "src" / "frontend"

    # TypeScript compilation test
    print("📝 TypeScript compilation test...")
    try:
        # Check if npx is available
        import shutil

        if shutil.which("npx"):
            result = subprocess.run(["npx", "tsc", "--noEmit"], capture_output=True, text=True, cwd=frontend_dir)
            if result.returncode == 0:
                print("✅ No TypeScript compilation errors")
            else:
                print("❌ TypeScript compilation errors found")
                print(f"Stderr: {result.stderr}")
        else:
            print("⚠️  npx not found - TypeScript compilation test skipped")
    except Exception as e:
        if "Sistem belirtilen dosyayı bulamıyor" in str(e) or "not found" in str(e).lower():
            print("⚠️  npx not found in PATH - TypeScript compilation test skipped")
        else:
            print(f"⚠️  TypeScript compilation test could not be performed: {e}")

    # Vite build test
    print("\n⚡ Vite build test...")
    try:
        # Check if npm is available
        import shutil

        if shutil.which("npm"):
            result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True, cwd=frontend_dir)
            if result.returncode == 0:
                print("✅ Vite build successful")
            else:
                print("❌ Vite build failed")
                print(f"Stderr: {result.stderr}")
        else:
            print("⚠️  npm not found - Vite build test skipped")
    except Exception as e:
        if "Sistem belirtilen dosyayı bulamıyor" in str(e) or "not found" in str(e).lower():
            print("⚠️  npm not found in PATH - Vite build test skipped")
        else:
            print(f"⚠️  Vite build test could not be performed: {e}")


def main():
    """Main test function"""
    print("🚀 Luminis AI Library Chatbot - Comprehensive Test Suite")
    print("=" * 60)
    print(f"📂 Project Directory: {project_root}")
    print(f"🐍 Python Version: {sys.version}")
    print("=" * 60)

    start_time = time.time()

    try:
        # Check project structure
        check_project_structure()

        # Check dependencies
        check_dependencies()

        # Run Python tests
        run_python_tests()

        # Run Node.js tests
        run_node_tests()

        # Run build tests
        run_build_tests()

    except KeyboardInterrupt:
        print("\n⚠️  Tests stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 60)
    print(f"⏱️  Total Test Duration: {duration:.2f} seconds")
    print("🎯 Test Suite completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
