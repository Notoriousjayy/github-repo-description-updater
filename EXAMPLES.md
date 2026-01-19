# Example Usage Guide

This guide provides real-world examples using your actual repositories.

## Setup

First, set your GitHub token:

```bash
# Linux/macOS
export GITHUB_TOKEN='ghp_your_token_here'

# Windows PowerShell
$env:GITHUB_TOKEN='ghp_your_token_here'
```

## Example 1: Quick Analysis

Analyze all your repositories and see suggestions:

```bash
python github_repo_description_updater.py --analyze
```

**Expected Output:**
```
================================================================================
REPOSITORY DESCRIPTION ANALYSIS REPORT
================================================================================
Generated: 2026-01-19 14:30:00
Total Repositories Analyzed: 37
================================================================================

1. c23-syntax-diagrams
--------------------------------------------------------------------------------
   Current:  (empty)
   Suggested: Interactive C23 language syntax diagrams with railroad visualizations and EBNF notation
   Language:  TypeScript
   Confidence: 95%
   Reasoning: Matched pattern: c23.*syntax.*diagram
   Topics: c23, syntax, railroad-diagrams

2. ghas-code-scanning-toolkit
--------------------------------------------------------------------------------
   Current:  (empty)
   Suggested: GitHub Advanced Security (GHAS) code scanning toolkit with automation utilities and best practices
   Language:  Python
   Confidence: 95%
   Reasoning: Matched pattern: ghas.*code.*scanning
...
```

## Example 2: Export Analysis to JSON

Export the analysis for review or further processing:

```bash
python github_repo_description_updater.py --analyze --export my_repos_analysis.json
```

**Sample JSON Output:**
```json
{
  "generated_at": "2026-01-19T14:30:00.000000",
  "total_repositories": 37,
  "analyses": [
    {
      "name": "c23-syntax-diagrams",
      "current_description": null,
      "suggested_description": "Interactive C23 language syntax diagrams with railroad visualizations and EBNF notation",
      "primary_language": "TypeScript",
      "topics": ["c23", "syntax", "railroad-diagrams"],
      "has_readme": true,
      "file_count": 25,
      "confidence": 0.95,
      "reasoning": "Matched pattern: c23.*syntax.*diagram"
    }
  ]
}
```

## Example 3: Dry Run - Preview Updates

See what would change without actually making updates:

```bash
python github_repo_description_updater.py --update-all --dry-run
```

**Expected Output:**
```
[DRY RUN] Would update c23-syntax-diagrams: 'Interactive C23 language syntax diagrams with railroad visualizations and EBNF notation'
[DRY RUN] Would update ghas-code-scanning-toolkit: 'GitHub Advanced Security (GHAS) code scanning toolkit with automation utilities and best practices'
[DRY RUN] Would update webgl2-wasm-pong: 'WebGL2 Pong game implementation using WebAssembly for high-performance rendering'
...
```

## Example 4: Update Only High-Confidence Suggestions

Update only repositories where we're very confident (≥85%):

```bash
python github_repo_description_updater.py --update-all --min-confidence 0.85
```

This will update:
- c23-syntax-diagrams
- JavaScript-Syntax-diagrams
- Python-syntax-diagrams
- Cpp23-Syntax-diagrams
- java21-syntax-diagrams
- ghas-code-scanning-toolkit
- WASM
- webgl2-wasm-pong
- cloud-computing-architecture-book-mapping

## Example 5: Update Only Empty Descriptions

Update repositories that don't have descriptions yet:

```bash
python github_repo_description_updater.py --update-all --skip-empty
```

This will skip:
- skills-change-commit-history (already has: "My copy of the skills course...")
- skills-introduction-to-codeql (already has: "Exercise: Introduction to CodeQL")
- skills-introduction-to-secret-scanning (already has: "GitHub Skills...")
- skills-secure-repository-supply-chain (already has: "Exercise: Secure...")

## Example 6: Update Specific Repositories

Update only your syntax diagram projects:

```bash
python github_repo_description_updater.py \
  --repos c23-syntax-diagrams JavaScript-Syntax-diagrams Python-syntax-diagrams \
         Cpp23-Syntax-diagrams java21-syntax-diagrams \
  --update
```

## Example 7: Update by Category

### Syntax Diagram Projects
```bash
python github_repo_description_updater.py \
  --repos c23-syntax-diagrams JavaScript-Syntax-diagrams \
         Python-syntax-diagrams Cpp23-Syntax-diagrams \
         java21-syntax-diagrams \
  --update
```

### Security Projects
```bash
python github_repo_description_updater.py \
  --repos ghas-code-scanning-toolkit \
  --update
```

### WebAssembly/Graphics Projects
```bash
python github_repo_description_updater.py \
  --repos WASM webgl2-wasm-pong Minimal-ModernOpenGL \
  --update
```

### Infrastructure Projects
```bash
python github_repo_description_updater.py \
  --repos terraform-aws-infra moodle-eks-terraform-blueprint \
         TerraDNS-Stack Nginx-web-proxy nginx-web-proxy-ui \
  --update
```

### Cloud Computing Documentation
```bash
python github_repo_description_updater.py \
  --repos cloud-computing-architecture-book-mapping \
         cloud-computing-book-mapping \
  --update
```

### Application Frameworks
```bash
python github_repo_description_updater.py \
  --repos ReactStreamline SpringStreamline \
  --update
```

## Example 8: Progressive Update Strategy

Step 1: Update very high confidence (95%+)
```bash
python github_repo_description_updater.py --update-all --min-confidence 0.95
```

Step 2: Review and update high confidence (85-94%)
```bash
python github_repo_description_updater.py --update-all --min-confidence 0.85 --dry-run
# Review output, then:
python github_repo_description_updater.py --update-all --min-confidence 0.85
```

Step 3: Review medium confidence (70-84%)
```bash
python github_repo_description_updater.py --update-all --min-confidence 0.70 --dry-run
# Manually review and decide
```

## Example 9: Complete Workflow with Backup

```bash
# Step 1: Create backup of current state
python github_repo_description_updater.py --analyze --export backup_$(date +%Y%m%d).json

# Step 2: Preview all changes
python github_repo_description_updater.py --update-all --dry-run

# Step 3: Update high-confidence items
python github_repo_description_updater.py --update-all --min-confidence 0.85

# Step 4: Verify changes
python github_repo_description_updater.py --analyze --export after_update_$(date +%Y%m%d).json

# Step 5: Compare (optional)
diff backup_*.json after_update_*.json
```

## Example 10: Using the Batch Operations Script

The batch operations script provides interactive workflows:

```bash
python batch_operations.py
```

**Menu:**
```
================================================================================
GitHub Repository Description Updater - Batch Operations
================================================================================

Available Workflows:
  1. Analyze and Export
  2. Progressive Updates (by confidence)
  3. Category-Based Updates
  4. Verify and Backup
  5. Update High-Priority Repos
  q. Quit

Select a workflow (1-5 or q):
```

## Example 11: Verify Specific Repository

Check what description would be suggested for a single repository:

```bash
python github_repo_description_updater.py --repos c23-syntax-diagrams --analyze
```

## Example 12: Update and Skip GitHub Skills Repos

GitHub Skills repositories already have good descriptions, so skip them:

```bash
# First, see which ones would be skipped
python github_repo_description_updater.py --update-all --skip-empty --dry-run

# Then update
python github_repo_description_updater.py --update-all --skip-empty
```

## Common Use Cases

### Use Case 1: New Repository Cleanup
You've just created several new repositories and want to add descriptions:

```bash
# See suggestions
python github_repo_description_updater.py --analyze

# Update only empty ones
python github_repo_description_updater.py --update-all --skip-empty --min-confidence 0.80
```

### Use Case 2: Improving Existing Descriptions
You want to improve all descriptions:

```bash
# See all suggestions (including for repos with descriptions)
python github_repo_description_updater.py --analyze

# Update all with high confidence
python github_repo_description_updater.py --update-all --min-confidence 0.90
```

### Use Case 3: Project Documentation
Export descriptions for documentation purposes:

```bash
python github_repo_description_updater.py --analyze --export project_catalog.json
```

Then use the JSON in your documentation system.

### Use Case 4: Standardizing Project Descriptions
Ensure all syntax diagram projects have consistent descriptions:

```bash
python github_repo_description_updater.py \
  --repos c23-syntax-diagrams JavaScript-Syntax-diagrams \
         Python-syntax-diagrams Cpp23-Syntax-diagrams \
         java21-syntax-diagrams \
  --update
```

## Tips and Best Practices

1. **Always start with dry-run**: Preview changes before applying
   ```bash
   --dry-run
   ```

2. **Use confidence thresholds**: Start high and work down
   ```bash
   --min-confidence 0.90  # Very confident
   --min-confidence 0.80  # Confident
   --min-confidence 0.70  # Somewhat confident
   ```

3. **Export for records**: Keep a record of changes
   ```bash
   --export analysis_$(date +%Y%m%d).json
   ```

4. **Update by category**: Group related repositories
   ```bash
   --repos syntax-repo1 syntax-repo2 syntax-repo3
   ```

5. **Check logs**: Review the log file for details
   ```bash
   tail -f repo_description_update.log
   ```

## Troubleshooting Examples

### Problem: Token not recognized
```bash
# Check if token is set
echo $GITHUB_TOKEN  # Linux/macOS
echo %GITHUB_TOKEN%  # Windows

# Set it properly
export GITHUB_TOKEN='ghp_your_token'
```

### Problem: Repository not found
```bash
# Check exact name
gh repo list  # Using GitHub CLI

# Use exact name from GitHub
python github_repo_description_updater.py --repos c23-syntax-diagrams --analyze
```

### Problem: Low confidence suggestions
```bash
# Review all suggestions first
python github_repo_description_updater.py --analyze --export review.json

# Manually review the JSON file
# Update only the ones you're confident about
python github_repo_description_updater.py --repos specific-repo --update
```

## Next Steps

After updating your repositories:

1. **Verify on GitHub**: Check that descriptions appear correctly
2. **Update topics**: Consider adding relevant topics to repositories
3. **Create README**: Ensure each repository has a good README
4. **Regular updates**: Re-run analysis periodically for new repositories

For more information, see README.md or:
```bash
python github_repo_description_updater.py --help
```
