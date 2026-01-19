# GitHub Repository Description Updater

A comprehensive Python script that intelligently analyzes your GitHub repositories and updates them with appropriate, descriptive names based on their content, structure, and purpose.

## Features

- **Intelligent Analysis**: Examines repository names, README content, primary languages, topics, and file structures
- **Pattern Matching**: Recognizes common project types (syntax diagrams, GHAS tools, WebAssembly projects, etc.)
- **Confidence Scoring**: Provides confidence levels for each suggested description
- **Dry Run Mode**: Preview changes before applying them
- **Selective Updates**: Update all repositories or specific ones
- **JSON Export**: Export analysis results for further processing
- **Comprehensive Logging**: Detailed logs for troubleshooting

## Installation

### Prerequisites

- Python 3.8 or higher
- A GitHub account with repositories
- A GitHub Personal Access Token with `repo` permissions

### Setup

1. Clone or download this script:
```bash
git clone <repository-url>
cd github-repo-description-updater
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install PyGithub requests
```

3. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a descriptive name (e.g., "Repo Description Updater")
   - Select the `repo` scope (Full control of private repositories)
   - Click "Generate token"
   - Copy the token immediately (you won't see it again!)

4. Set your token as an environment variable:
```bash
# Linux/macOS
export GITHUB_TOKEN='your_token_here'

# Windows (PowerShell)
$env:GITHUB_TOKEN='your_token_here'

# Windows (Command Prompt)
set GITHUB_TOKEN=your_token_here
```

## Usage

### Basic Usage

#### 1. Analyze All Repositories
Get suggestions for all your repositories without making changes:
```bash
python github_repo_description_updater.py --analyze
```

#### 2. Analyze and Export to JSON
```bash
python github_repo_description_updater.py --analyze --export analysis.json
```

#### 3. Dry Run - Preview Updates
See what would be changed without actually updating:
```bash
python github_repo_description_updater.py --update-all --dry-run
```

#### 4. Update All Repositories
Apply suggested descriptions to all repositories:
```bash
python github_repo_description_updater.py --update-all
```

#### 5. Update Specific Repositories
Update only certain repositories:
```bash
python github_repo_description_updater.py --repos c23-syntax-diagrams ghas-code-scanning-toolkit --update
```

### Advanced Usage

#### Update Only High-Confidence Suggestions
Only update repositories where the confidence is 80% or higher:
```bash
python github_repo_description_updater.py --update-all --min-confidence 0.8
```

#### Skip Repositories That Already Have Descriptions
Only update repositories with empty descriptions:
```bash
python github_repo_description_updater.py --update-all --skip-empty
```

#### Specify GitHub Token via Command Line
```bash
python github_repo_description_updater.py --token YOUR_TOKEN --analyze
```

#### Analyze Another User's Public Repositories
```bash
python github_repo_description_updater.py --username other-user --analyze
```

### Complete Example Workflow

Here's a recommended workflow for updating your repository descriptions:

```bash
# Step 1: Analyze and review suggestions
python github_repo_description_updater.py --analyze

# Step 2: Export analysis to review offline
python github_repo_description_updater.py --analyze --export my_analysis.json

# Step 3: Preview what would be updated (dry run)
python github_repo_description_updater.py --update-all --dry-run

# Step 4: Update only high-confidence suggestions
python github_repo_description_updater.py --update-all --min-confidence 0.85

# Step 5: Update remaining repositories individually if needed
python github_repo_description_updater.py --repos specific-repo --update
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `--token TOKEN` | GitHub personal access token (or use GITHUB_TOKEN env var) |
| `--username USER` | GitHub username to analyze (defaults to authenticated user) |
| `--analyze` | Analyze repositories and show suggestions |
| `--update-all` | Update all repositories with suggested descriptions |
| `--update` | Update specified repositories (use with `--repos`) |
| `--repos REPO1 REPO2 ...` | List of repository names to process |
| `--dry-run` | Simulate updates without making changes |
| `--export FILE` | Export analysis to JSON file |
| `--min-confidence N` | Minimum confidence threshold for updates (0.0-1.0) |
| `--skip-empty` | Skip repositories that already have descriptions |

## How It Works

### Analysis Process

The script uses a multi-stage analysis approach:

1. **Pattern Matching**: Checks repository names against known patterns (syntax diagrams, GHAS tools, etc.)
   - Confidence: 95%

2. **README Analysis**: Extracts descriptions from README files
   - Confidence: 85%

3. **Metadata Analysis**: Generates descriptions from language and topics
   - Confidence: 70%

4. **Name-Based Generation**: Creates descriptions from repository names
   - Confidence: 50%

### Recognized Repository Types

The script has built-in recognition for:

- **Syntax Diagram Projects**: C23, JavaScript, Python, C++23, Java21
- **Security Tools**: GHAS code scanning, secret scanning
- **Graphics Projects**: WebGL, WebAssembly, OpenGL
- **Infrastructure**: Terraform, AWS, Nginx
- **Frameworks**: React, Spring Boot
- **Educational**: GitHub Skills courses
- **Games**: Pong implementations, learning games

## Output

### Console Output

The script provides detailed console output:

```
2026-01-19 10:30:00 - INFO - Authenticated as: Notoriousjayy
2026-01-19 10:30:01 - INFO - Processing 37 repositories...
2026-01-19 10:30:02 - INFO - Analyzing repository: c23-syntax-diagrams
...

================================================================================
REPOSITORY DESCRIPTION ANALYSIS REPORT
================================================================================
Generated: 2026-01-19 10:30:15
Total Repositories Analyzed: 37
================================================================================

1. c23-syntax-diagrams
--------------------------------------------------------------------------------
   Current:  (empty)
   Suggested: Interactive C23 language syntax diagrams with railroad visualizations and EBNF notation
   Language:  TypeScript
   Confidence: 95%
   Reasoning: Matched pattern: c23.*syntax.*diagram
   Topics: c23, syntax, diagrams, railroad

...
```

### JSON Export

Example JSON output structure:

```json
{
  "generated_at": "2026-01-19T10:30:15.123456",
  "total_repositories": 37,
  "analyses": [
    {
      "name": "c23-syntax-diagrams",
      "current_description": null,
      "suggested_description": "Interactive C23 language syntax diagrams with railroad visualizations and EBNF notation",
      "primary_language": "TypeScript",
      "topics": ["c23", "syntax", "diagrams"],
      "has_readme": true,
      "file_count": 25,
      "confidence": 0.95,
      "reasoning": "Matched pattern: c23.*syntax.*diagram"
    }
  ]
}
```

### Log Files

All operations are logged to `repo_description_update.log`:

```
2026-01-19 10:30:00,123 - INFO - Authenticated as: Notoriousjayy
2026-01-19 10:30:01,456 - INFO - Processing 37 repositories...
2026-01-19 10:30:02,789 - INFO - Analyzing repository: c23-syntax-diagrams
2026-01-19 10:30:05,012 - INFO - ✓ Updated c23-syntax-diagrams: 'Interactive C23 language syntax diagrams...'
```

## Customization

### Adding Custom Patterns

To add custom description patterns, edit the `DESCRIPTION_PATTERNS` dictionary in the script:

```python
DESCRIPTION_PATTERNS = {
    # Your custom patterns
    r'my.*custom.*pattern': 'Description for repositories matching this pattern',
    r'another.*pattern': 'Another custom description',
    
    # Existing patterns...
}
```

Patterns use Python regular expressions (regex).

### Adjusting Confidence Thresholds

You can modify the confidence levels in the `_generate_description` method:

```python
def _generate_description(self, repo, has_readme, primary_language, topics):
    # Pattern match
    return (description, 0.95, "reason")  # High confidence
    
    # README extraction
    return (description, 0.85, "reason")  # Good confidence
    
    # Metadata generation
    return (description, 0.70, "reason")  # Medium confidence
    
    # Generic
    return (description, 0.50, "reason")  # Low confidence
```

## Troubleshooting

### Common Issues

#### "Error: GitHub token required"
**Solution**: Ensure your token is set via `--token` or the `GITHUB_TOKEN` environment variable.

#### "Repository not found"
**Solution**: 
- Check that you have access to the repository
- Verify the repository name is spelled correctly
- Ensure your token has the necessary permissions

#### "Rate limit exceeded"
**Solution**: 
- GitHub API has rate limits (5,000 requests/hour for authenticated requests)
- Wait for the rate limit to reset
- Consider processing repositories in batches

#### "Permission denied"
**Solution**: 
- Ensure your token has `repo` scope
- For organization repositories, you need admin access
- Regenerate your token if permissions were changed

### Debug Mode

Enable debug logging by modifying the script:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    ...
)
```

## Best Practices

1. **Always use dry-run first**: Preview changes before applying them
   ```bash
   python github_repo_description_updater.py --update-all --dry-run
   ```

2. **Export analysis for review**: Save suggestions for offline review
   ```bash
   python github_repo_description_updater.py --analyze --export review.json
   ```

3. **Use confidence thresholds**: Start with high confidence (0.8+) and gradually lower
   ```bash
   python github_repo_description_updater.py --update-all --min-confidence 0.8
   ```

4. **Process in batches**: For many repositories, process them in groups
   ```bash
   python github_repo_description_updater.py --repos repo1 repo2 repo3 --update
   ```

5. **Keep your token secure**: 
   - Never commit tokens to version control
   - Use environment variables
   - Rotate tokens regularly
   - Use fine-grained tokens when possible

## Security Considerations

- **Token Security**: Your GitHub token has powerful permissions. Never share it or commit it to version control.
- **Scope Limitation**: The script only requires `repo` scope. Don't grant unnecessary permissions.
- **Audit Changes**: Review the dry-run output before applying changes.
- **Backup**: GitHub maintains history, but consider exporting current descriptions before bulk updates.

## Contributing

Contributions are welcome! Areas for improvement:

- Additional language/framework recognition patterns
- Enhanced README parsing
- Support for GitHub Enterprise
- Bulk operations optimization
- AI-powered description generation

## License

MIT License - Feel free to use and modify as needed.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the log file (`repo_description_update.log`)
3. Run with `--dry-run` to diagnose issues
4. Open an issue with detailed error messages and logs

## Acknowledgments

Built for efficient GitHub repository management with intelligent automation.

---

**Note**: This script modifies your GitHub repositories. Always review suggestions before applying updates.
