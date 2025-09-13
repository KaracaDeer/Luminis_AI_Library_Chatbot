#!/bin/bash

# Git History Cleanup Script for Luminis.AI Library Assistant
# ===========================================================
#
# This script helps clean up git commit history by:
# 1. Squashing commits
# 2. Removing unnecessary files
# 3. Creating a clean commit structure
#
# Usage:
#   ./scripts/cleanup_git_history.sh [options]
#
# Options:
#   --interactive    Interactive rebase for commit squashing
#   --clean-files    Remove unnecessary files from history
#   --reset-hard     Hard reset to clean state (DANGEROUS)
#   --backup         Create backup branch before cleanup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_BRANCH="backup-before-cleanup"
MAIN_BRANCH="main"

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        error "Not in a git repository"
        exit 1
    fi
}

# Create backup branch
create_backup() {
    log "Creating backup branch: $BACKUP_BRANCH"
    git branch $BACKUP_BRANCH
    success "Backup branch created: $BACKUP_BRANCH"
}

# Clean unnecessary files
clean_files() {
    log "Cleaning unnecessary files..."

    # Remove common unnecessary files
    local files_to_remove=(
        "*.pyc"
        "*.pyo"
        "*.pyd"
        "__pycache__/"
        ".pytest_cache/"
        ".coverage"
        "coverage.xml"
        "htmlcov/"
        "*.log"
        ".DS_Store"
        "Thumbs.db"
        "*.tmp"
        "*.temp"
        "node_modules/"
        ".npm"
        ".yarn"
        "dist/"
        "build/"
        ".next/"
        ".nuxt/"
        "*.egg-info/"
        ".mypy_cache/"
        ".tox/"
        ".nox/"
        "*.swp"
        "*.swo"
        "*~"
        ".vscode/settings.json"
        ".idea/workspace.xml"
        ".idea/tasks.xml"
        ".idea/usage.statistics.xml"
        ".idea/dictionaries"
        ".idea/shelf"
    )

    for pattern in "${files_to_remove[@]}"; do
        if git ls-files --error-unmatch "$pattern" > /dev/null 2>&1; then
            log "Removing: $pattern"
            git rm -r --cached "$pattern" 2>/dev/null || true
        fi
    done

    success "Files cleaned"
}

# Interactive rebase for commit squashing
interactive_rebase() {
    local commit_count=${1:-10}

    log "Starting interactive rebase for last $commit_count commits"
    warn "This will open an editor. Please follow the instructions to squash commits."

    git rebase -i HEAD~$commit_count

    success "Interactive rebase completed"
}

# Reset to clean state (DANGEROUS)
reset_hard() {
    warn "This will permanently delete all uncommitted changes!"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log "Performing hard reset..."
        git reset --hard HEAD
        git clean -fd
        success "Hard reset completed"
    else
        log "Reset cancelled"
    fi
}

# Optimize repository
optimize_repo() {
    log "Optimizing repository..."

    # Garbage collect
    git gc --prune=now --aggressive

    # Repack objects
    git repack -a -d --depth=250 --window=250

    success "Repository optimized"
}

# Show commit statistics
show_stats() {
    log "Commit statistics:"
    echo "Total commits: $(git rev-list --count HEAD)"
    echo "Total files: $(git ls-files | wc -l)"
    echo "Repository size: $(du -sh .git | cut -f1)"
    echo "Last 10 commits:"
    git log --oneline -10
}

# Main cleanup function
main_cleanup() {
    local interactive=false
    local clean_files_flag=false
    local reset_hard_flag=false
    local backup_flag=false
    local commit_count=10

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --interactive)
                interactive=true
                shift
                ;;
            --clean-files)
                clean_files_flag=true
                shift
                ;;
            --reset-hard)
                reset_hard_flag=true
                shift
                ;;
            --backup)
                backup_flag=true
                shift
                ;;
            --commits)
                commit_count="$2"
                shift 2
                ;;
            -h|--help)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  --interactive    Interactive rebase for commit squashing"
                echo "  --clean-files    Remove unnecessary files from history"
                echo "  --reset-hard     Hard reset to clean state (DANGEROUS)"
                echo "  --backup         Create backup branch before cleanup"
                echo "  --commits N      Number of commits to rebase (default: 10)"
                echo "  -h, --help       Show this help message"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    check_git_repo

    log "Starting git history cleanup..."

    # Create backup if requested
    if [[ "$backup_flag" == true ]]; then
        create_backup
    fi

    # Clean files if requested
    if [[ "$clean_files_flag" == true ]]; then
        clean_files
    fi

    # Interactive rebase if requested
    if [[ "$interactive" == true ]]; then
        interactive_rebase "$commit_count"
    fi

    # Reset hard if requested
    if [[ "$reset_hard_flag" == true ]]; then
        reset_hard
    fi

    # Optimize repository
    optimize_repo

    # Show final statistics
    show_stats

    success "Git history cleanup completed!"

    if [[ "$backup_flag" == true ]]; then
        log "Backup branch available: $BACKUP_BRANCH"
        log "To restore: git reset --hard $BACKUP_BRANCH"
    fi
}

# Run main function
main_cleanup "$@"
