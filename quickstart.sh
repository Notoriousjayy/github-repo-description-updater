#!/bin/bash
# Quick Start Guide for GitHub Repository Description Updater
# ============================================================

echo "GitHub Repository Description Updater - Quick Start"
echo "===================================================="
echo ""

# Step 1: Check Python version
echo "Step 1: Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi
echo "✓ Python 3 is installed"
echo ""

# Step 2: Install dependencies
echo "Step 2: Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Step 3: Check for GitHub token
echo "Step 3: Checking for GitHub token..."
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠ GITHUB_TOKEN environment variable is not set"
    echo ""
    echo "To set your token:"
    echo "  Linux/macOS: export GITHUB_TOKEN='your_token_here'"
    echo "  Windows PowerShell: \$env:GITHUB_TOKEN='your_token_here'"
    echo ""
    echo "To create a token:"
    echo "  1. Go to https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token (classic)'"
    echo "  3. Give it a name (e.g., 'Repo Description Updater')"
    echo "  4. Select the 'repo' scope"
    echo "  5. Click 'Generate token'"
    echo "  6. Copy the token and set it as an environment variable"
    echo ""
    read -p "Enter your GitHub token now (or press Enter to skip): " token
    if [ ! -z "$token" ]; then
        export GITHUB_TOKEN="$token"
        echo "✓ Token set for this session"
    else
        echo "⚠ Skipping token setup - you'll need to set it later"
    fi
else
    echo "✓ GITHUB_TOKEN is set"
fi
echo ""

# Step 4: Test the script
echo "Step 4: Testing the script with a dry run..."
echo ""
read -p "Press Enter to analyze your repositories (no changes will be made)..."

python3 github_repo_description_updater.py --analyze

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Script execution failed"
    echo "Please check the error messages above"
    exit 1
fi

echo ""
echo "===================================================="
echo "Quick Start Complete!"
echo "===================================================="
echo ""
echo "Next Steps:"
echo "1. Review the analysis output above"
echo "2. To preview updates without making changes:"
echo "   python3 github_repo_description_updater.py --update-all --dry-run"
echo ""
echo "3. To update only high-confidence suggestions:"
echo "   python3 github_repo_description_updater.py --update-all --min-confidence 0.8"
echo ""
echo "4. To export analysis to JSON:"
echo "   python3 github_repo_description_updater.py --analyze --export analysis.json"
echo ""
echo "5. To update specific repositories:"
echo "   python3 github_repo_description_updater.py --repos repo1 repo2 --update"
echo ""
echo "For more options, see README.md or run:"
echo "   python3 github_repo_description_updater.py --help"
echo ""
