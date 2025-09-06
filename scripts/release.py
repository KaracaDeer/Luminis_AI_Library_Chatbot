#!/usr/bin/env python3
"""
Release script for Luminis AI Library Assistant
==============================================

This script automates the release process by:
1. Updating version numbers across all files
2. Creating git tags
3. Generating release notes
4. Preparing for GitHub release

Usage:
    python scripts/release.py --version 1.1.0
    python scripts/release.py --patch
    python scripts/release.py --minor
    python scripts/release.py --major
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def get_current_version():
    """Get current version from VERSION file"""
    version_file = PROJECT_ROOT / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "1.0.0"


def update_version_file(new_version):
    """Update VERSION file"""
    version_file = PROJECT_ROOT / "VERSION"
    version_file.write_text(f"{new_version}\n", encoding="utf-8")
    print(f"✅ Updated VERSION file: {new_version}")


def update_python_version(new_version):
    """Update Python version file"""
    version_file = PROJECT_ROOT / "src" / "__version__.py"
    if version_file.exists():
        content = version_file.read_text()

        # Update version string
        content = re.sub(
            r'__version__ = "[^"]*"', f'__version__ = "{new_version}"', content
        )

        # Update version info tuple
        version_parts = new_version.split(".")
        version_tuple = f"({version_parts[0]}, {version_parts[1]}, {version_parts[2]})"
        content = re.sub(
            r"__version_info__ = \([^)]*\)",
            f"__version_info__ = {version_tuple}",
            content,
        )

        version_file.write_text(content, encoding="utf-8")
        print(f"✅ Updated Python version file: {new_version}")


def update_package_json(new_version, file_path):
    """Update package.json version"""
    if file_path.exists():
        with open(file_path, "r") as f:
            data = json.load(f)

        data["version"] = new_version

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Updated {file_path.name}: {new_version}")


def update_all_versions(new_version):
    """Update version in all relevant files"""
    print(f"🔄 Updating version to {new_version}...")

    # Update VERSION file
    update_version_file(new_version)

    # Update Python version
    update_python_version(new_version)

    # Update package.json files
    update_package_json(new_version, PROJECT_ROOT / "package.json")
    update_package_json(new_version, PROJECT_ROOT / "src" / "frontend" / "package.json")

    print(f"✅ All version files updated to {new_version}")


def increment_version(current_version, increment_type):
    """Increment version based on type"""
    parts = current_version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if increment_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif increment_type == "minor":
        minor += 1
        patch = 0
    elif increment_type == "patch":
        patch += 1

    return f"{major}.{minor}.{patch}"


def create_git_tag(version, message=None):
    """Create git tag for version"""
    if message is None:
        message = f"Release version {version}"

    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True, cwd=PROJECT_ROOT)

        # Commit changes
        subprocess.run(
            ["git", "commit", "-m", f"chore: bump version to {version}"],
            check=True,
            cwd=PROJECT_ROOT,
        )

        # Create tag
        subprocess.run(
            ["git", "tag", "-a", f"v{version}", "-m", message],
            check=True,
            cwd=PROJECT_ROOT,
        )

        print(f"✅ Created git tag v{version}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create git tag: {e}")
        return False


def generate_release_notes(version):
    """Generate release notes"""
    notes = f"""# Release v{version}

## 🚀 What's New

### Features
- AI-powered library assistant
- Multilingual support (Turkish/English)
- Book recommendations and analysis
- User authentication and profiles
- OAuth 2.0 integration
- Voice message support
- Docker containerization

### Technical Improvements
- FastAPI backend with async support
- React frontend with TypeScript
- Vector database integration
- Comprehensive test suite
- GitHub Actions CI/CD
- Docker Compose setup

## 📦 Installation

### Docker (Recommended)
```bash
git clone https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot.git
cd Luminis_AI_Library_Chatbot
docker-compose up -d
```

### Manual Installation
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd src/frontend
npm install
npm run build
```

## 🔧 Configuration

1. Copy `.env.example` to `.env`
2. Set your OpenAI API key
3. Configure database settings
4. Run the application

## 📚 Documentation

- [README.md](README.md)
- [API Documentation](docs/)
- [Contributing Guide](CONTRIBUTING.md)

## 🐛 Bug Reports

Please report bugs via [GitHub Issues](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/issues)

---
*Released on {datetime.now().strftime('%Y-%m-%d')}*
"""

    release_notes_file = PROJECT_ROOT / f"RELEASE_NOTES_v{version}.md"
    release_notes_file.write_text(notes, encoding="utf-8")
    print(f"✅ Generated release notes: {release_notes_file.name}")

    return release_notes_file


def main():
    parser = argparse.ArgumentParser(
        description="Release script for Luminis AI Library Assistant"
    )
    parser.add_argument("--version", help="Specific version to release")
    parser.add_argument("--major", action="store_true", help="Increment major version")
    parser.add_argument("--minor", action="store_true", help="Increment minor version")
    parser.add_argument("--patch", action="store_true", help="Increment patch version")
    parser.add_argument("--tag", action="store_true", help="Create git tag")
    parser.add_argument("--notes", action="store_true", help="Generate release notes")
    parser.add_argument("--message", help="Custom tag message")

    args = parser.parse_args()

    current_version = get_current_version()
    print(f"📋 Current version: {current_version}")

    # Determine new version
    if args.version:
        new_version = args.version
    elif args.major:
        new_version = increment_version(current_version, "major")
    elif args.minor:
        new_version = increment_version(current_version, "minor")
    elif args.patch:
        new_version = increment_version(current_version, "patch")
    else:
        print("❌ Please specify version increment type or specific version")
        sys.exit(1)

    print(f"🎯 New version: {new_version}")

    # Update versions
    update_all_versions(new_version)

    # Generate release notes
    if args.notes:
        generate_release_notes(new_version)

    # Create git tag
    if args.tag:
        create_git_tag(new_version, args.message)

    print(f"\n🎉 Release preparation completed for v{new_version}")
    print("\nNext steps:")
    print("1. Review changes: git diff")
    print("2. Push to GitHub: git push origin main --tags")
    print("3. Create GitHub release with generated notes")


if __name__ == "__main__":
    main()
