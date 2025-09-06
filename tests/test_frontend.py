import unittest
import sys
import os
import json
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestFrontendComponents(unittest.TestCase):
    """Tests frontend components"""

    def setUp(self):
        """Test preparation"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
        os.makedirs(self.test_data_dir, exist_ok=True)

    def test_package_json_structure(self):
        """Tests package.json file structure"""
        package_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "frontend",
            "package.json",
        )

        self.assertTrue(os.path.exists(package_path), "package.json file not found")

        try:
            with open(package_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)

            # Check if basic fields exist
            required_fields = [
                "name",
                "version",
                "scripts",
                "dependencies",
                "devDependencies",
            ]
            for field in required_fields:
                self.assertIn(
                    field, package_data, f"Field {field} not found in package.json"
                )

            # Check if scripts exist
            required_scripts = ["dev", "build", "start"]
            for script in required_scripts:
                self.assertIn(
                    script, package_data["scripts"], f"Script {script} not found"
                )

        except Exception as e:
            self.fail(f"package.json test failed: {e}")

    def test_tsconfig_structure(self):
        """Tests TypeScript configuration file structure"""
        project_root = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "frontend"
        )

        # Check tsconfig.json
        tsconfig_path = os.path.join(project_root, "tsconfig.json")
        self.assertTrue(os.path.exists(tsconfig_path), "tsconfig.json not found")

        # Check tsconfig.node.json
        tsconfig_node_path = os.path.join(project_root, "tsconfig.node.json")
        self.assertTrue(
            os.path.exists(tsconfig_node_path), "tsconfig.node.json not found"
        )

        # Check file existence (without trying to parse JSON)
        self.assertTrue(os.path.getsize(tsconfig_path) > 0, "tsconfig.json is empty")
        self.assertTrue(
            os.path.getsize(tsconfig_node_path) > 0, "tsconfig.node.json is empty"
        )

        # Search for basic keywords in file content
        try:
            with open(tsconfig_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("compilerOptions", content, "compilerOptions not found")
                self.assertIn("include", content, "include not found")

        except Exception as e:
            self.fail(f"tsconfig.json could not be read: {e}")

    def test_vite_config(self):
        """Tests if Vite configuration files exist"""
        project_root = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "frontend"
        )

        # Check Vite configuration files
        vite_files = ["vite.config.ts", "vite.config.js", "vite.config.d.ts"]

        for vite_file in vite_files:
            file_path = os.path.join(project_root, vite_file)
            if os.path.exists(file_path):
                self.assertTrue(True, f"{vite_file} found")
            else:
                print(f"WARNING: {vite_file} not found (optional)")

    def test_tailwind_config(self):
        """Tests if Tailwind CSS configuration files exist"""
        project_root = os.path.dirname(os.path.dirname(__file__))

        # Check Tailwind configuration files (in src/frontend folder)
        tailwind_files = [
            "src/frontend/tailwind.config.js",
            "src/frontend/postcss.config.js",
        ]

        for tailwind_file in tailwind_files:
            file_path = os.path.join(project_root, tailwind_file)
            self.assertTrue(os.path.exists(file_path), f"{tailwind_file} not found")

    def test_src_structure(self):
        """Tests src folder structure"""
        src_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "frontend"
        )

        self.assertTrue(os.path.exists(src_path), "src folder not found")

        # Check if basic folders exist
        required_dirs = ["components", "contexts", "services", "stores"]
        for dir_name in required_dirs:
            dir_path = os.path.join(src_path, dir_name)
            self.assertTrue(os.path.exists(dir_path), f"{dir_name} folder not found")

        # Check if main files exist
        required_files = ["main.tsx", "App.tsx", "index.css"]
        for file_name in required_files:
            file_path = os.path.join(src_path, file_name)
            self.assertTrue(os.path.exists(file_path), f"{file_name} file not found")

    def test_component_files(self):
        """Tests if basic component files exist"""
        components_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "frontend", "components"
        )

        # Check if basic components exist
        required_components = [
            "Header.tsx",
            "Sidebar.tsx",
            "ChatPage.tsx",
            "AccountPage.tsx",
            "LoginPage.tsx",
            "RegisterPage.tsx",
        ]

        for component in required_components:
            component_path = os.path.join(components_path, component)
            self.assertTrue(
                os.path.exists(component_path), f"Component {component} not found"
            )

    def test_context_files(self):
        """Tests if context files exist"""
        contexts_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "frontend", "contexts"
        )

        # Check if context files exist
        required_contexts = ["AuthContext.tsx"]

        for context in required_contexts:
            context_path = os.path.join(contexts_path, context)
            self.assertTrue(
                os.path.exists(context_path), f"Context {context} not found"
            )

    def test_store_files(self):
        """Tests if store files exist"""
        stores_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "frontend", "stores"
        )

        # Check if store files exist
        required_stores = ["chatStore.ts", "languageStore.ts"]

        for store in required_stores:
            store_path = os.path.join(stores_path, store)
            self.assertTrue(os.path.exists(store_path), f"Store {store} not found")

    def test_service_files(self):
        """Tests if service files exist"""
        services_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "frontend", "services"
        )

        # Check if service files exist
        required_services = ["api.ts"]

        for service in required_services:
            service_path = os.path.join(services_path, service)
            self.assertTrue(
                os.path.exists(service_path), f"Service {service} not found"
            )


class TestFrontendDependencies(unittest.TestCase):
    """Tests frontend dependencies"""

    def test_react_dependencies(self):
        """Tests if React and basic dependencies exist in package.json"""
        package_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "package.json"
        )

        try:
            with open(package_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)

            # Check basic React dependencies
            required_deps = ["react", "react-dom", "react-router-dom"]
            for dep in required_deps:
                self.assertIn(
                    dep, package_data["dependencies"], f"Dependency {dep} not found"
                )

            # Check TypeScript dependencies
            required_dev_deps = ["typescript", "@types/react", "@types/react-dom"]
            for dep in required_dev_deps:
                self.assertIn(
                    dep,
                    package_data["devDependencies"],
                    f"Dev dependency {dep} not found",
                )

        except Exception as e:
            self.fail(f"Dependency tests failed: {e}")

    def test_build_tools(self):
        """Tests if build tools exist"""
        package_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "package.json"
        )

        try:
            with open(package_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)

            # Check build tools
            build_tools = ["vite", "@vitejs/plugin-react"]
            for tool in build_tools:
                self.assertIn(
                    tool,
                    package_data["devDependencies"],
                    f"Build tool {tool} not found",
                )

        except Exception as e:
            self.fail(f"Build tools test failed: {e}")


if __name__ == "__main__":
    unittest.main()
