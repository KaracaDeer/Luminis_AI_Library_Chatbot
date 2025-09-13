#!/usr/bin/env python3
"""
Comprehensive Test Runner for Luminis.AI Library Assistant
=========================================================

This script runs all tests in the project with proper reporting and coverage.
It handles both Python backend tests and frontend tests, providing a unified
testing experience.

Usage:
    python tests/run_comprehensive_tests.py [options]

Options:
    --backend-only    Run only backend tests
    --frontend-only   Run only frontend tests
    --coverage        Generate coverage reports
    --verbose         Verbose output
    --parallel        Run tests in parallel
    --fail-fast       Stop on first failure
"""

import os
import sys
import subprocess
import argparse
import json
import time
from pathlib import Path
from typing import List, Dict, Optional


class TestRunner:
    """Comprehensive test runner for the Luminis.AI project"""

    def __init__(self, verbose: bool = False, fail_fast: bool = False):
        self.verbose = verbose
        self.fail_fast = fail_fast
        self.project_root = Path(__file__).parent.parent
        self.results = {
            "backend": {"passed": 0, "failed": 0, "skipped": 0, "errors": []},
            "frontend": {"passed": 0, "failed": 0, "skipped": 0, "errors": []},
            "total_time": 0,
        }

    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def run_command(
        self, command: List[str], cwd: Optional[Path] = None
    ) -> subprocess.CompletedProcess:
        """Run a command and return the result"""
        if cwd is None:
            cwd = self.project_root

        if self.verbose:
            self.log(f"Running: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            return result
        except subprocess.TimeoutExpired:
            self.log("Command timed out after 5 minutes", "ERROR")
            raise

    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        self.log("Checking dependencies...")

        # Check Python dependencies
        try:
            import pytest
            import fastapi
            import sqlalchemy

            self.log("✓ Python dependencies found")
        except ImportError as e:
            self.log(f"✗ Missing Python dependency: {e}", "ERROR")
            return False

        # Check Node.js dependencies
        frontend_path = self.project_root / "src" / "frontend"
        if frontend_path.exists():
            package_json = frontend_path / "package.json"
            if package_json.exists():
                self.log("✓ Frontend package.json found")
            else:
                self.log("✗ Frontend package.json not found", "WARNING")

        return True

    def run_backend_tests(self, coverage: bool = False) -> bool:
        """Run backend Python tests"""
        self.log("Running backend tests...")

        test_files = [
            "tests/test_backend.py",
            "tests/test_backend_endpoints.py",
            "tests/test_services.py",
            "tests/test_integration.py",
            "tests/test_frontend_components.py",
        ]

        # Filter existing test files
        existing_tests = []
        for test_file in test_files:
            test_path = self.project_root / test_file
            if test_path.exists():
                existing_tests.append(test_file)

        if not existing_tests:
            self.log("No backend test files found", "WARNING")
            return True

        # Build pytest command
        cmd = ["python", "-m", "pytest", "-v"]

        if self.fail_fast:
            cmd.append("-x")

        if coverage:
            cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])

        cmd.extend(existing_tests)

        try:
            result = self.run_command(cmd)

            if result.returncode == 0:
                self.log("✓ Backend tests passed")
                self.results["backend"]["passed"] = 1
                return True
            else:
                self.log("✗ Backend tests failed", "ERROR")
                self.results["backend"]["failed"] = 1
                if self.verbose:
                    print("STDOUT:", result.stdout)
                    print("STDERR:", result.stderr)
                return False

        except Exception as e:
            self.log(f"✗ Backend test execution failed: {e}", "ERROR")
            self.results["backend"]["errors"].append(str(e))
            return False

    def run_frontend_tests(self) -> bool:
        """Run frontend tests"""
        self.log("Running frontend tests...")

        frontend_path = self.project_root / "src" / "frontend"
        if not frontend_path.exists():
            self.log("Frontend directory not found", "WARNING")
            return True

        # Check if package.json exists
        package_json = frontend_path / "package.json"
        if not package_json.exists():
            self.log("Frontend package.json not found", "WARNING")
            return True

        # Try to run frontend tests
        try:
            # Check if test script exists
            with open(package_json, "r") as f:
                package_data = json.load(f)

            scripts = package_data.get("scripts", {})
            if "test" not in scripts:
                self.log("No test script found in frontend package.json", "WARNING")
                return True

            # Run frontend tests
            result = self.run_command(["npm", "test"], cwd=frontend_path)

            if result.returncode == 0:
                self.log("✓ Frontend tests passed")
                self.results["frontend"]["passed"] = 1
                return True
            else:
                self.log("✗ Frontend tests failed", "ERROR")
                self.results["frontend"]["failed"] = 1
                if self.verbose:
                    print("STDOUT:", result.stdout)
                    print("STDERR:", result.stderr)
                return False

        except Exception as e:
            self.log(f"✗ Frontend test execution failed: {e}", "ERROR")
            self.results["frontend"]["errors"].append(str(e))
            return False

    def run_type_checking(self) -> bool:
        """Run TypeScript type checking"""
        self.log("Running TypeScript type checking...")

        frontend_path = self.project_root / "src" / "frontend"
        if not frontend_path.exists():
            self.log("Frontend directory not found", "WARNING")
            return True

        try:
            result = self.run_command(["npm", "run", "type-check"], cwd=frontend_path)

            if result.returncode == 0:
                self.log("✓ TypeScript type checking passed")
                return True
            else:
                self.log("✗ TypeScript type checking failed", "ERROR")
                if self.verbose:
                    print("STDOUT:", result.stdout)
                    print("STDERR:", result.stderr)
                return False

        except Exception as e:
            self.log(f"✗ TypeScript type checking failed: {e}", "ERROR")
            return False

    def run_linting(self) -> bool:
        """Run code linting"""
        self.log("Running code linting...")

        # Python linting (if available)
        try:
            result = self.run_command(["python", "-m", "flake8", "src/", "tests/"])
            if result.returncode == 0:
                self.log("✓ Python linting passed")
            else:
                self.log("✗ Python linting issues found", "WARNING")
        except FileNotFoundError:
            self.log("flake8 not found, skipping Python linting", "INFO")

        # Frontend linting
        frontend_path = self.project_root / "src" / "frontend"
        if frontend_path.exists():
            try:
                result = self.run_command(["npm", "run", "lint"], cwd=frontend_path)
                if result.returncode == 0:
                    self.log("✓ Frontend linting passed")
                else:
                    self.log("✗ Frontend linting issues found", "WARNING")
            except Exception as e:
                self.log(f"Frontend linting failed: {e}", "WARNING")

        return True

    def generate_report(self) -> None:
        """Generate test report"""
        self.log("Generating test report...")

        total_passed = (
            self.results["backend"]["passed"] + self.results["frontend"]["passed"]
        )
        total_failed = (
            self.results["backend"]["failed"] + self.results["frontend"]["failed"]
        )
        total_errors = len(self.results["backend"]["errors"]) + len(
            self.results["frontend"]["errors"]
        )

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    LUMINIS.AI TEST REPORT                    ║
╠══════════════════════════════════════════════════════════════╣
║ Backend Tests:  {'PASSED' if self.results['backend']['passed'] else 'FAILED':<10} ║
║ Frontend Tests: {'PASSED' if self.results['frontend']['passed'] else 'FAILED':<9} ║
║ Total Time:     {self.results['total_time']:.2f}s{'':<10} ║
╠══════════════════════════════════════════════════════════════╣
║ Summary:                                                    ║
║   • Passed: {total_passed}                                                    ║
║   • Failed: {total_failed}                                                    ║
║   • Errors: {total_errors}                                                    ║
╚══════════════════════════════════════════════════════════════╝
        """

        print(report)

        # Save detailed report
        report_file = self.project_root / "test_report.json"
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)

        self.log(f"Detailed report saved to: {report_file}")

    def run_all_tests(
        self,
        backend_only: bool = False,
        frontend_only: bool = False,
        coverage: bool = False,
    ) -> bool:
        """Run all tests"""
        start_time = time.time()

        self.log("Starting comprehensive test suite...")

        if not self.check_dependencies():
            self.log("Dependency check failed", "ERROR")
            return False

        success = True

        # Run backend tests
        if not frontend_only:
            if not self.run_backend_tests(coverage=coverage):
                success = False
                if self.fail_fast:
                    return False

        # Run frontend tests
        if not backend_only:
            if not self.run_frontend_tests():
                success = False
                if self.fail_fast:
                    return False

        # Run type checking
        if not backend_only:
            if not self.run_type_checking():
                success = False
                if self.fail_fast:
                    return False

        # Run linting
        if not self.run_linting():
            success = False

        self.results["total_time"] = time.time() - start_time
        self.generate_report()

        return success


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Comprehensive Test Runner for Luminis.AI"
    )
    parser.add_argument(
        "--backend-only", action="store_true", help="Run only backend tests"
    )
    parser.add_argument(
        "--frontend-only", action="store_true", help="Run only frontend tests"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage reports"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--fail-fast", "-x", action="store_true", help="Stop on first failure"
    )

    args = parser.parse_args()

    runner = TestRunner(verbose=args.verbose, fail_fast=args.fail_fast)

    success = runner.run_all_tests(
        backend_only=args.backend_only,
        frontend_only=args.frontend_only,
        coverage=args.coverage,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
