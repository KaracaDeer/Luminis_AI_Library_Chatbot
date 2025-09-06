# 🏷️ Release Guide

This guide explains how to create and manage releases for the Luminis AI Library Assistant project.

## 📋 Release Process

### 1. Version Types

- **Patch** (1.0.0 → 1.0.1): Bug fixes, minor improvements
- **Minor** (1.0.0 → 1.1.0): New features, backward compatible
- **Major** (1.0.0 → 2.0.0): Breaking changes, major updates

### 2. Creating a Release

#### Using the Release Script

```bash
# Patch release (bug fixes)
python scripts/release.py --patch --notes --tag

# Minor release (new features)
python scripts/release.py --minor --notes --tag

# Major release (breaking changes)
python scripts/release.py --major --notes --tag

# Specific version
python scripts/release.py --version 1.2.0 --notes --tag
```

#### Manual Process

1. **Update version numbers:**
   ```bash
   python scripts/release.py --patch
   ```

2. **Generate release notes:**
   ```bash
   python scripts/release.py --notes
   ```

3. **Create git tag:**
   ```bash
   python scripts/release.py --tag --message "Release v1.0.1 with bug fixes"
   ```

4. **Push to GitHub:**
   ```bash
   git push origin main --tags
   ```

### 3. GitHub Actions Release

The release workflow automatically triggers when you push a tag:

```bash
# Create and push tag
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1
```

This will:
- Run all tests
- Build Docker images
- Create GitHub release
- Generate release notes

### 4. Release Checklist

Before creating a release:

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version numbers are consistent
- [ ] Release notes are generated
- [ ] Docker images build successfully
- [ ] No breaking changes (for minor/patch)

### 5. Version Files

The release script updates these files:

- `VERSION` - Main version file
- `src/__version__.py` - Python version
- `package.json` - Root package version
- `src/frontend/package.json` - Frontend version

### 6. Release Notes Template

Release notes include:

- 🚀 What's New
- 📦 Installation instructions
- 🔧 Configuration guide
- 📚 Documentation links
- 🐛 Bug report information

### 7. GitHub Release

After pushing tags, GitHub Actions will:

1. Run comprehensive tests
2. Build frontend
3. Create Docker images
4. Generate release notes
5. Create GitHub release
6. Upload artifacts

### 8. Rollback

If a release has issues:

```bash
# Revert to previous version
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1

# Update version files
python scripts/release.py --version 1.0.0
```

## 🔧 Troubleshooting

### Common Issues

1. **Version conflict:**
   ```bash
   # Check current version
   cat VERSION
   
   # Update to specific version
   python scripts/release.py --version 1.0.1
   ```

2. **Git tag already exists:**
   ```bash
   # Delete existing tag
   git tag -d v1.0.1
   git push origin :refs/tags/v1.0.1
   ```

3. **Release notes not generated:**
   ```bash
   # Generate manually
   python scripts/release.py --notes
   ```

## 📚 Best Practices

1. **Semantic Versioning:** Follow semver.org guidelines
2. **Release Notes:** Always include what's new and breaking changes
3. **Testing:** Ensure all tests pass before release
4. **Documentation:** Update docs with new features
5. **Backward Compatibility:** Consider impact on existing users

## 🆘 Support

For release-related issues:

- Check [GitHub Issues](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/issues)
- Review [CONTRIBUTING.md](../CONTRIBUTING.md)
- Contact the development team
