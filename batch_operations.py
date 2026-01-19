#!/usr/bin/env python3
"""
Example Batch Operations for Repository Description Updates
============================================================
This script demonstrates various batch operations and workflows
for managing repository descriptions at scale.
"""

import os
import sys
import json
import subprocess
from datetime import datetime


def run_command(cmd):
    """Execute a shell command and return output."""
    print(f"\n{'='*80}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*80}\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result.returncode == 0


def workflow_1_analyze_and_export():
    """Workflow 1: Analyze all repositories and export results."""
    print("\n" + "="*80)
    print("WORKFLOW 1: Analyze and Export")
    print("="*80)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"analysis_{timestamp}.json"
    
    cmd = [
        "python3", "github_repo_description_updater.py",
        "--analyze",
        "--export", output_file
    ]
    
    if run_command(cmd):
        print(f"\n✓ Analysis exported to: {output_file}")
        
        # Load and display summary
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        print(f"\nSummary:")
        print(f"  Total repositories: {data['total_repositories']}")
        
        # Count by confidence
        high_conf = sum(1 for a in data['analyses'] if a['confidence'] >= 0.8)
        med_conf = sum(1 for a in data['analyses'] if 0.6 <= a['confidence'] < 0.8)
        low_conf = sum(1 for a in data['analyses'] if a['confidence'] < 0.6)
        
        print(f"  High confidence (≥80%): {high_conf}")
        print(f"  Medium confidence (60-79%): {med_conf}")
        print(f"  Low confidence (<60%): {low_conf}")
    else:
        print("\n✗ Analysis failed")


def workflow_2_progressive_updates():
    """Workflow 2: Progressive updates starting with highest confidence."""
    print("\n" + "="*80)
    print("WORKFLOW 2: Progressive Updates")
    print("="*80)
    
    # Step 1: Update very high confidence (95%+)
    print("\nStep 1: Updating very high confidence suggestions (95%+)")
    cmd = [
        "python3", "github_repo_description_updater.py",
        "--update-all",
        "--min-confidence", "0.95",
        "--dry-run"
    ]
    run_command(cmd)
    
    input("\nPress Enter to continue with actual updates...")
    
    cmd[-1] = "--skip-empty"  # Replace --dry-run with --skip-empty
    run_command(cmd)
    
    # Step 2: Update high confidence (80-94%)
    print("\nStep 2: Updating high confidence suggestions (80-94%)")
    cmd = [
        "python3", "github_repo_description_updater.py",
        "--update-all",
        "--min-confidence", "0.80",
        "--skip-empty"
    ]
    run_command(cmd)
    
    # Step 3: Update medium confidence (70-79%)
    print("\nStep 3: Review medium confidence suggestions (70-79%)")
    print("These require manual review before updating.")
    cmd = [
        "python3", "github_repo_description_updater.py",
        "--update-all",
        "--min-confidence", "0.70",
        "--dry-run"
    ]
    run_command(cmd)


def workflow_3_category_updates():
    """Workflow 3: Update repositories by category."""
    print("\n" + "="*80)
    print("WORKFLOW 3: Category-Based Updates")
    print("="*80)
    
    categories = {
        "Syntax Diagrams": [
            "c23-syntax-diagrams",
            "JavaScript-Syntax-diagrams",
            "Python-syntax-diagrams",
            "Cpp23-Syntax-diagrams",
            "java21-syntax-diagrams"
        ],
        "Security Tools": [
            "ghas-code-scanning-toolkit"
        ],
        "WebAssembly/Graphics": [
            "WASM",
            "webgl2-wasm-pong",
            "Minimal-ModernOpenGL"
        ],
        "Infrastructure": [
            "terraform-aws-infra",
            "moodle-eks-terraform-blueprint",
            "TerraDNS-Stack",
            "Nginx-web-proxy",
            "nginx-web-proxy-ui"
        ],
        "Application Templates": [
            "ReactStreamline",
            "SpringStreamline"
        ]
    }
    
    for category, repos in categories.items():
        print(f"\nUpdating category: {category}")
        print(f"Repositories: {', '.join(repos)}")
        
        cmd = [
            "python3", "github_repo_description_updater.py",
            "--repos"
        ] + repos + [
            "--update",
            "--dry-run"
        ]
        
        run_command(cmd)
        
        response = input("\nApply these updates? (y/n): ")
        if response.lower() == 'y':
            cmd[-1] = ""  # Remove --dry-run
            run_command(cmd[:-1])  # Run without dry-run flag


def workflow_4_verify_and_rollback():
    """Workflow 4: Verification workflow with rollback capability."""
    print("\n" + "="*80)
    print("WORKFLOW 4: Verify Updates")
    print("="*80)
    
    # First, export current state
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_before_update_{timestamp}.json"
    
    print("\nCreating backup of current descriptions...")
    cmd = [
        "python3", "github_repo_description_updater.py",
        "--analyze",
        "--export", backup_file
    ]
    
    if run_command(cmd):
        print(f"\n✓ Backup created: {backup_file}")
        print("You can use this to verify changes or rollback if needed.")
    
    # Preview updates
    print("\nPreviewing updates...")
    cmd = [
        "python3", "github_repo_description_updater.py",
        "--update-all",
        "--min-confidence", "0.80",
        "--dry-run"
    ]
    run_command(cmd)
    
    response = input("\nProceed with updates? (y/n): ")
    if response.lower() == 'y':
        cmd[-1] = ""  # Remove --dry-run
        run_command(cmd[:-1])
        
        # Export new state
        after_file = f"state_after_update_{timestamp}.json"
        cmd = [
            "python3", "github_repo_description_updater.py",
            "--analyze",
            "--export", after_file
        ]
        run_command(cmd)
        
        print(f"\n✓ New state exported: {after_file}")
        print(f"To compare: diff {backup_file} {after_file}")


def workflow_5_specific_repos():
    """Workflow 5: Update specific high-priority repositories."""
    print("\n" + "="*80)
    print("WORKFLOW 5: High-Priority Repository Updates")
    print("="*80)
    
    priority_repos = [
        "c23-syntax-diagrams",
        "ghas-code-scanning-toolkit",
        "ReactStreamline",
        "cloud-computing-architecture-book-mapping"
    ]
    
    print("\nHigh-priority repositories:")
    for repo in priority_repos:
        print(f"  - {repo}")
    
    print("\nAnalyzing these repositories...")
    cmd = [
        "python3", "github_repo_description_updater.py",
        "--repos"
    ] + priority_repos + [
        "--analyze"
    ]
    
    if run_command(cmd):
        response = input("\nUpdate these repositories? (y/n): ")
        if response.lower() == 'y':
            cmd = [
                "python3", "github_repo_description_updater.py",
                "--repos"
            ] + priority_repos + [
                "--update"
            ]
            run_command(cmd)


def main():
    """Main menu for batch operations."""
    print("\n" + "="*80)
    print("GitHub Repository Description Updater - Batch Operations")
    print("="*80)
    
    workflows = {
        "1": ("Analyze and Export", workflow_1_analyze_and_export),
        "2": ("Progressive Updates (by confidence)", workflow_2_progressive_updates),
        "3": ("Category-Based Updates", workflow_3_category_updates),
        "4": ("Verify and Backup", workflow_4_verify_and_rollback),
        "5": ("Update High-Priority Repos", workflow_5_specific_repos),
    }
    
    print("\nAvailable Workflows:")
    for key, (name, _) in workflows.items():
        print(f"  {key}. {name}")
    print("  q. Quit")
    
    choice = input("\nSelect a workflow (1-5 or q): ").strip()
    
    if choice.lower() == 'q':
        print("Exiting...")
        sys.exit(0)
    
    if choice in workflows:
        _, workflow_func = workflows[choice]
        workflow_func()
        
        input("\nPress Enter to continue...")
        main()  # Return to menu
    else:
        print("Invalid choice. Please try again.")
        main()


if __name__ == "__main__":
    # Check for GitHub token
    if not os.environ.get('GITHUB_TOKEN'):
        print("\nError: GITHUB_TOKEN environment variable is not set")
        print("Please set your GitHub token before running batch operations.")
        print("\nExample:")
        print("  export GITHUB_TOKEN='your_token_here'")
        sys.exit(1)
    
    main()
