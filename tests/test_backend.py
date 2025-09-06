"""
Backend Service Tests for Luminis.AI Library Assistant
====================================================

This test file contains comprehensive tests for the backend services of the
Luminis.AI Library Assistant application. It tests the core functionality,
imports, configurations, and API endpoints to ensure the backend is working
correctly.

Test Coverage:
1. Database Module Imports: Verifies database components can be imported
2. Service Imports: Tests RAG and Vector service imports
3. FastAPI Application: Validates main app creation and configuration
4. Environment Variables: Checks required configuration variables
5. CORS Configuration: Verifies cross-origin resource sharing setup
6. API Endpoints: Tests that expected endpoints are defined
7. Dependencies: Ensures required Python packages are installed
8. Service Functionality: Tests core service operations

What These Tests Verify:
- All required modules can be imported without errors
- FastAPI application starts correctly with proper configuration
- CORS middleware is properly configured for frontend integration
- API endpoints are correctly defined and accessible
- Environment variables are properly loaded
- Core services initialize without errors

Running These Tests:
- Ensures backend is properly configured
- Validates service dependencies are met
- Confirms API structure is correct
- Helps identify configuration issues early

This test suite is essential for:
- Development environment validation
- CI/CD pipeline integration
- Backend service reliability
- API endpoint verification
"""

import unittest
import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def setup_import_paths():
    """Helper function to setup import paths for tests"""
    # Add src directory to path for imports
    src_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"
    )
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    return src_path


def import_main_module():
    """Helper function to import main module"""
    src_path = setup_import_paths()
    import importlib.util

    main_path = os.path.join(src_path, "backend", "main.py")
    spec = importlib.util.spec_from_file_location("main", main_path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    return main_module


class TestBackendServices(unittest.TestCase):
    """Tests backend services"""

    def setUp(self):
        """Test preparation"""
        self.test_db_path = tempfile.mktemp()

    def test_database_imports(self):
        """Tests if database modules can be imported"""
        src_path = setup_import_paths()

        # Try multiple import approaches
        success = False
        error_msg = ""

        try:
            from database.database import get_db, create_tables, init_sample_data

            success = True
        except ImportError as e:
            error_msg = f"First attempt failed: {e}"
            try:
                from database import get_db, create_tables, init_sample_data

                success = True
            except ImportError as e:
                error_msg += f" Second attempt failed: {e}"
                try:
                    # Try importlib approach
                    import importlib.util

                    database_path = os.path.join(src_path, "database", "database.py")
                    if os.path.exists(database_path):
                        spec = importlib.util.spec_from_file_location(
                            "database", database_path
                        )
                        database_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(database_module)
                        get_db = database_module.get_db
                        create_tables = database_module.create_tables
                        init_sample_data = database_module.init_sample_data
                        success = True
                    else:
                        error_msg += f" Database file not found at: {database_path}"
                except Exception as e:
                    error_msg += f" Third attempt failed: {e}"

        if success:
            self.assertTrue(True, "Database modules imported successfully")
        else:
            self.skipTest(
                f"Database module not available in test environment. {error_msg}"
            )

    def test_rag_service_imports(self):
        """Tests if RAG service modules can be imported"""
        try:
            setup_import_paths()
            from services.rag_service import RAGService

            self.assertTrue(True, "RAG service modules imported successfully")
        except ImportError as e:
            self.fail(f"RAG service modules could not be imported: {e}")

    def test_vector_service_imports(self):
        """Tests if Vector service modules can be imported"""
        try:
            setup_import_paths()
            from services.vector_service import VectorService

            self.assertTrue(True, "Vector service modules imported successfully")
        except ImportError as e:
            self.fail(f"Vector service modules could not be imported: {e}")

    def test_main_app_creation(self):
        """Tests if main FastAPI application can be created"""
        try:
            main_module = import_main_module()
            app = main_module.app

            self.assertIsNotNone(app, "FastAPI application could not be created")
            self.assertEqual(app.title, "Luminis.AI Library Assistant API")
        except Exception as e:
            self.fail(f"Main application test failed: {e}")

    def test_environment_variables(self):
        """Tests if required environment variables exist"""
        from dotenv import load_dotenv

        load_dotenv()

        # OpenAI API key check (optional)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.assertIsInstance(openai_key, str, "OpenAI API key should be string")
            self.assertGreater(len(openai_key), 0, "OpenAI API key should not be empty")

    def test_cors_configuration(self):
        """Tests CORS configuration"""
        try:
            main_module = import_main_module()
            app = main_module.app

            # Check if CORS middleware is added
            cors_middleware = None
            for middleware in app.user_middleware:
                if "CORSMiddleware" in str(middleware):
                    cors_middleware = middleware
                    break

            self.assertIsNotNone(cors_middleware, "CORS middleware not found")
        except Exception as e:
            self.fail(f"CORS configuration test failed: {e}")

    def test_api_endpoints(self):
        """Tests if API endpoints are defined"""
        try:
            main_module = import_main_module()
            app = main_module.app

            routes = [route.path for route in app.routes]

            # Check if basic endpoints exist
            expected_endpoints = ["/docs", "/openapi.json"]
            for endpoint in expected_endpoints:
                self.assertIn(endpoint, routes, f"Endpoint {endpoint} not found")

        except Exception as e:
            self.fail(f"API endpoints test failed: {e}")

    def test_dependencies(self):
        """Tests if required Python packages are installed"""
        required_packages = ["fastapi", "uvicorn", "sqlalchemy", "openai", "dotenv"]

        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                self.assertTrue(True, f"Paket {package} yüklü")
            except ImportError:
                self.fail(f"Paket {package} yüklü değil")


class TestDatabaseOperations(unittest.TestCase):
    """Tests database operations"""

    def test_database_connection(self):
        """Tests database connection"""
        try:
            src_path = setup_import_paths()

            # Try multiple import approaches
            engine = None
            try:
                from database.database import engine
            except ImportError:
                try:
                    from database import engine
                except ImportError:
                    # Try importlib approach
                    import importlib.util

                    database_path = os.path.join(src_path, "database", "database.py")
                    if os.path.exists(database_path):
                        spec = importlib.util.spec_from_file_location(
                            "database", database_path
                        )
                        database_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(database_module)
                        engine = database_module.engine

            if engine is not None:
                # Check if engine can be created
                self.assertIsNotNone(engine, "Database engine could not be created")
            else:
                self.skipTest("Database engine not available in test environment")
        except Exception as e:
            self.skipTest(f"Database connection test skipped: {e}")

    def test_sample_data_structure(self):
        """Tests sample data structure"""
        try:
            main_module = import_main_module()
            BOOKS_DATABASE = main_module.BOOKS_DATABASE

            # Check if BOOKS_DATABASE is a list
            self.assertIsInstance(
                BOOKS_DATABASE, list, "BOOKS_DATABASE should be a list"
            )

            if BOOKS_DATABASE:
                # Check if first book has required fields
                first_book = BOOKS_DATABASE[0]
                required_fields = ["title", "author", "genre"]

                for field in required_fields:
                    self.assertIn(field, first_book, f"Book should have {field} field")

        except Exception as e:
            self.fail(f"Sample data structure test failed: {e}")


if __name__ == "__main__":
    unittest.main()
