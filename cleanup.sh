#!/bin/bash
# Cleanup Script for AnalyzingGithub Project
# ==========================================
# This script removes Windows Zone.Identifier files, cleans Python cache, and
# organizes common generated artifacts into exports/, logs/, and backups/.

echo "GitHub Repo Description Updater - Cleanup Script"
echo "================================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_info() { echo "ℹ $1"; }

# Check if we're in the right directory
if [ ! -f "github_repo_description_updater.py" ]; then
    print_error "Error: Run this script from the AnalyzingGithub directory"
    exit 1
fi

print_info "Current directory: $(pwd)"
echo ""

# Step 1: Remove Zone.Identifier files
echo "Step 1: Removing Windows Zone.Identifier files..."
mapfile -t zone_files < <(find . -name "*:Zone.Identifier" -type f 2>/dev/null)
zone_count=${#zone_files[@]}

if [ "$zone_count" -gt 0 ]; then
    for file in "${zone_files[@]}"; do
        if [ -f "$file" ]; then
            rm -f -- "$file"
            print_success "Removed: $(basename "$file")"
        fi
    done
    print_success "Removed $zone_count Zone.Identifier file(s)"
else
    print_info "No Zone.Identifier files found"
fi
echo ""

# Step 2: Remove Python cache
echo "Step 2: Cleaning Python cache..."
cache_dirs_count=$(find . -type d -name "__pycache__" -print 2>/dev/null | wc -l | tr -d ' ')
cache_files_count=$(find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -print 2>/dev/null | wc -l | tr -d ' ')

if [ "$cache_dirs_count" -gt 0 ] || [ "$cache_files_count" -gt 0 ]; then
    find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null
    find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete 2>/dev/null
    print_success "Python cache cleaned"
else
    print_info "No Python cache files found"
fi
echo ""

# Step 3: Create necessary directories
echo "Step 3: Creating project structure..."
mkdir -p exports logs backups 2>/dev/null

if [ -d "exports" ] && [ -d "logs" ] && [ -d "backups" ]; then
    print_success "Created directories: exports/, logs/, backups/"
else
    print_warning "Some directories may already exist"
fi
echo ""

# Step 4: Organize files
echo "Step 4: Organizing files..."

# Move JSON exports
json_count=0
shopt -s nullglob
json_files=(my_github_catalog_*.json analysis_*.json backup_*.json)
for file in "${json_files[@]}"; do
    if [ -f "$file" ]; then
        mv -f -- "$file" exports/ 2>/dev/null && ((json_count++))
    fi
done
shopt -u nullglob

if [ "$json_count" -gt 0 ]; then
    print_success "Moved $json_count JSON export(s) to exports/"
else
    print_info "No JSON exports to move"
fi

# Move log files (any *.log in the project root)
log_count=0
shopt -s nullglob
log_files=( *.log )
for file in "${log_files[@]}"; do
    if [ -f "$file" ]; then
        mv -f -- "$file" logs/ 2>/dev/null && ((log_count++))
    fi
done
shopt -u nullglob

if [ "$log_count" -gt 0 ]; then
    print_success "Moved $log_count log file(s) to logs/"
else
    print_info "No log files to move"
fi
echo ""

# Step 5: Set permissions
echo "Step 5: Setting file permissions..."
if [ -f "quickstart.sh" ]; then
    chmod +x quickstart.sh
    print_success "Made quickstart.sh executable"
fi

if [ -f "batch_operations.py" ]; then
    chmod +x batch_operations.py
    print_success "Made batch_operations.py executable"
fi

if [ -f "github_repo_description_updater.py" ]; then
    chmod +x github_repo_description_updater.py
    print_success "Made github_repo_description_updater.py executable"
fi
echo ""

# Step 6: Verify .gitignore
echo "Step 6: Verifying .gitignore..."
if [ ! -f ".gitignore" ]; then
    print_warning ".gitignore not found - you should add it"
else
    print_success ".gitignore exists"
fi
echo ""

# Step 7: Summary
echo "================================================="
echo "Cleanup Complete!"
echo "================================================="
echo ""
echo "Project Structure:"
tree -L 1 -a 2>/dev/null || ls -la
echo ""

# Show git status if in a git repo
if [ -d ".git" ]; then
    echo "Git Status:"
    git status --short
    echo ""
fi

echo "Next Steps:"
echo "  1. Review the cleaned directory"
echo "  2. Initialize git: git init"
echo "  3. Add files: git add ."
echo "  4. Commit: git commit -m 'Initial commit'"
echo ""
echo "To remove old exports/logs:"
echo "  rm -rf exports/* logs/*"
echo ""
