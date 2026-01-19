@echo off
REM Quick Start Guide for GitHub Repository Description Updater (Windows)
REM ====================================================================

echo GitHub Repository Description Updater - Quick Start (Windows)
echo ==============================================================
echo.

REM Step 1: Check Python version
echo Step 1: Checking Python version...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo [OK] Python is installed
echo.

REM Step 2: Install dependencies
echo Step 2: Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Step 3: Check for GitHub token
echo Step 3: Checking for GitHub token...
if "%GITHUB_TOKEN%"=="" (
    echo [WARNING] GITHUB_TOKEN environment variable is not set
    echo.
    echo To set your token for this session:
    echo   set GITHUB_TOKEN=your_token_here
    echo.
    echo To set it permanently:
    echo   setx GITHUB_TOKEN "your_token_here"
    echo.
    echo To create a token:
    echo   1. Go to https://github.com/settings/tokens
    echo   2. Click 'Generate new token (classic^)'
    echo   3. Give it a name (e.g., 'Repo Description Updater'^)
    echo   4. Select the 'repo' scope
    echo   5. Click 'Generate token'
    echo   6. Copy the token and set it as an environment variable
    echo.
    set /p token="Enter your GitHub token now (or press Enter to skip): "
    if not "%token%"=="" (
        set GITHUB_TOKEN=%token%
        echo [OK] Token set for this session
    ) else (
        echo [WARNING] Skipping token setup - you'll need to set it later
    )
) else (
    echo [OK] GITHUB_TOKEN is set
)
echo.

REM Step 4: Test the script
echo Step 4: Testing the script with analysis...
echo.
pause Press any key to analyze your repositories (no changes will be made^)...

python github_repo_description_updater.py --analyze

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Script execution failed
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Quick Start Complete!
echo ============================================================
echo.
echo Next Steps:
echo 1. Review the analysis output above
echo 2. To preview updates without making changes:
echo    python github_repo_description_updater.py --update-all --dry-run
echo.
echo 3. To update only high-confidence suggestions:
echo    python github_repo_description_updater.py --update-all --min-confidence 0.8
echo.
echo 4. To export analysis to JSON:
echo    python github_repo_description_updater.py --analyze --export analysis.json
echo.
echo 5. To update specific repositories:
echo    python github_repo_description_updater.py --repos repo1 repo2 --update
echo.
echo For more options, see README.md or run:
echo    python github_repo_description_updater.py --help
echo.
pause
