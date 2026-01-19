#!/usr/bin/env python3
"""
GitHub Repository Renamer
==========================
Rename GitHub repositories with descriptive, SEO-friendly names using gh CLI.

Author: Jordan Suber
Date: January 2026
"""

import os
import sys
import json
import argparse
import logging
import subprocess
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('repo_rename.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class RenameProposal:
    """Data class for repository rename proposals."""
    current_name: str
    new_name: str
    reason: str
    priority: str  # 'high', 'medium', 'low'
    confidence: float
    category: str
    
    def is_valid_name(self) -> bool:
        """Check if the new name is valid for GitHub."""
        # GitHub repo name rules:
        # - Max 100 characters
        # - Alphanumeric, hyphens, underscores, dots
        # - Cannot start/end with special characters
        if len(self.new_name) > 100:
            return False
        
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]$'
        return bool(re.match(pattern, self.new_name))


class RepositoryRenamer:
    """Handles renaming of GitHub repositories using gh CLI."""
    
    # Predefined rename mappings with improved names
    RENAME_MAPPINGS = {
        # Documentation Projects
        'Building-Microservices': {
            'new_name': 'microservices-architecture-guide',
            'reason': 'More descriptive and SEO-friendly',
            'category': 'Documentation',
            'priority': 'high'
        },
        'Understanding-ETL': {
            'new_name': 'etl-patterns-and-practices',
            'reason': 'Clearer purpose and searchable',
            'category': 'Documentation',
            'priority': 'high'
        },
        'CIFlowDocs': {
            'new_name': 'cicd-pipeline-documentation',
            'reason': 'Expanded acronym for clarity',
            'category': 'Documentation',
            'priority': 'high'
        },
        'CISSP': {
            'new_name': 'cissp-study-guide',
            'reason': 'Clear purpose for certification prep',
            'category': 'Education',
            'priority': 'high'
        },
        
        # Development Tools
        'dev-guidelines': {
            'new_name': 'software-development-guidelines',
            'reason': 'More descriptive and professional',
            'category': 'Documentation',
            'priority': 'medium'
        },
        'Mathematical-Utility-API': {
            'new_name': 'math-utilities-api',
            'reason': 'Shorter, cleaner, more standard',
            'category': 'API',
            'priority': 'medium'
        },
        
        # Game Projects
        'Pong': {
            'new_name': 'pong-game-python',
            'reason': 'Adds language context for clarity',
            'category': 'Games',
            'priority': 'low'
        },
        'TechTeensPong': {
            'new_name': 'tech-teens-pong-tutorial',
            'reason': 'Clarifies educational purpose',
            'category': 'Education',
            'priority': 'medium'
        },
        'Binaryville': {
            'new_name': 'binaryville-learning-game',
            'reason': 'Adds context about learning focus',
            'category': 'Education',
            'priority': 'low'
        },
        
        # Graphics Projects
        'WASM': {
            'new_name': 'webassembly-examples',
            'reason': 'Expanded acronym and added context',
            'category': 'Graphics',
            'priority': 'high'
        },
        'webgl2-wasm-pong': {
            'new_name': 'webgl2-wasm-pong-game',
            'reason': 'Minor clarity improvement',
            'category': 'Graphics',
            'priority': 'low'
        },
        'Minimal-ModernOpenGL': {
            'new_name': 'modern-opengl-examples',
            'reason': 'Cleaner, more standard naming',
            'category': 'Graphics',
            'priority': 'medium'
        },
        'C_Base_GSL_OpenGL_project': {
            'new_name': 'c-gsl-opengl-graphics',
            'reason': 'Cleaner naming, removed underscores',
            'category': 'Graphics',
            'priority': 'high'
        },
        
        # Infrastructure
        'Nginx-web-proxy': {
            'new_name': 'nginx-reverse-proxy-config',
            'reason': 'More specific and descriptive',
            'category': 'Infrastructure',
            'priority': 'low'
        },
        'nginx-web-proxy-ui': {
            'new_name': 'nginx-proxy-management-ui',
            'reason': 'Clearer purpose',
            'category': 'Infrastructure',
            'priority': 'low'
        },
        'TerraDNS-Stack': {
            'new_name': 'terraform-dns-infrastructure',
            'reason': 'Expanded and clarified',
            'category': 'Infrastructure',
            'priority': 'low'
        },
        
        # Security
        'ComplyMatrix-Security-Standards': {
            'new_name': 'compliance-matrix-security',
            'reason': 'Shorter and cleaner',
            'category': 'Security',
            'priority': 'low'
        },
        
        # Application Templates
        'ReactStreamline': {
            'new_name': 'react-starter-template',
            'reason': 'Standard naming convention',
            'category': 'Templates',
            'priority': 'medium'
        },
        'SpringStreamline': {
            'new_name': 'spring-boot-starter-template',
            'reason': 'Standard naming convention',
            'category': 'Templates',
            'priority': 'medium'
        },
        
        # Utilities
        'Matrix-Element-Randomizer': {
            'new_name': 'matrix-randomizer-utility',
            'reason': 'Shorter while maintaining clarity',
            'category': 'Utilities',
            'priority': 'low'
        },
        'notification-batch-processor': {
            'new_name': 'notification-batch-service',
            'reason': 'More standard service naming',
            'category': 'Services',
            'priority': 'low'
        },
        
        # Keep these as-is or minor changes
        # Syntax diagram projects are already well-named
        # GHAS toolkit is already well-named
        # Terraform projects are already well-named
        # GitHub Skills repos should not be renamed
    }
    
    def __init__(self, username: str, dry_run: bool = True):
        """
        Initialize the repository renamer.
        
        Args:
            username: GitHub username
            dry_run: If True, only simulate renames
        """
        self.username = username
        self.dry_run = dry_run
        self.check_gh_cli()
        logger.info(f"Repository Renamer initialized for {username} (dry_run={dry_run})")
    
    def check_gh_cli(self):
        """Check if gh CLI is installed and authenticated."""
        try:
            result = subprocess.run(
                ['gh', 'auth', 'status'],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                logger.error("gh CLI is not authenticated")
                logger.error("Please run: gh auth login")
                sys.exit(1)
            
            logger.info("✓ gh CLI is installed and authenticated")
            
        except FileNotFoundError:
            logger.error("gh CLI is not installed")
            logger.error("Install from: https://cli.github.com/")
            sys.exit(1)
    
    def generate_rename_proposals(
        self, 
        analysis_file: Optional[str] = None
    ) -> List[RenameProposal]:
        """
        Generate rename proposals for repositories.
        
        Args:
            analysis_file: Path to analysis JSON file (optional)
            
        Returns:
            List of rename proposals
        """
        proposals = []
        
        # Load analysis data if provided
        analysis_data = None
        if analysis_file and os.path.exists(analysis_file):
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
        
        # Generate proposals from predefined mappings
        for current_name, rename_info in self.RENAME_MAPPINGS.items():
            proposal = RenameProposal(
                current_name=current_name,
                new_name=rename_info['new_name'],
                reason=rename_info['reason'],
                priority=rename_info['priority'],
                confidence=0.95,  # High confidence for manual mappings
                category=rename_info['category']
            )
            
            if proposal.is_valid_name():
                proposals.append(proposal)
            else:
                logger.warning(f"Invalid name proposed for {current_name}: {proposal.new_name}")
        
        return proposals
    
    def check_name_availability(self, new_name: str) -> bool:
        """
        Check if a repository name is available.
        
        Args:
            new_name: Proposed new repository name
            
        Returns:
            True if available, False otherwise
        """
        try:
            result = subprocess.run(
                ['gh', 'repo', 'view', f"{self.username}/{new_name}"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # If return code is 0, repo exists (name not available)
            return result.returncode != 0
            
        except Exception as e:
            logger.error(f"Error checking availability: {e}")
            return False
    
    def rename_repository(self, proposal: RenameProposal) -> bool:
        """
        Rename a repository using gh CLI.
        
        Args:
            proposal: RenameProposal object
            
        Returns:
            True if successful, False otherwise
        """
        current_full = f"{self.username}/{proposal.current_name}"
        new_name = proposal.new_name
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Would rename: {proposal.current_name} → {new_name}")
            logger.info(f"           Reason: {proposal.reason}")
            return True
        
        try:
            # Check if new name is available
            if not self.check_name_availability(new_name):
                logger.error(f"✗ Name already exists: {new_name}")
                return False
            
            # Execute rename
            result = subprocess.run(
                ['gh', 'repo', 'rename', new_name, '--repo', current_full, '--yes'],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                logger.info(f"✓ Renamed: {proposal.current_name} → {new_name}")
                return True
            else:
                logger.error(f"✗ Failed to rename {proposal.current_name}")
                logger.error(f"  Error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Exception renaming {proposal.current_name}: {str(e)}")
            return False
    
    def batch_rename(
        self, 
        proposals: List[RenameProposal],
        priority_filter: Optional[str] = None
    ) -> Tuple[int, int]:
        """
        Rename multiple repositories.
        
        Args:
            proposals: List of rename proposals
            priority_filter: Only rename repos with this priority ('high', 'medium', 'low')
            
        Returns:
            Tuple of (successful_count, failed_count)
        """
        if priority_filter:
            proposals = [p for p in proposals if p.priority == priority_filter]
        
        successful = 0
        failed = 0
        
        for proposal in proposals:
            if self.rename_repository(proposal):
                successful += 1
            else:
                failed += 1
        
        return successful, failed


def export_rename_plan(proposals: List[RenameProposal], output_file: str):
    """Export rename proposals to JSON file."""
    data = {
        'generated_at': datetime.now().isoformat(),
        'total_proposals': len(proposals),
        'proposals': [
            {
                'current_name': p.current_name,
                'new_name': p.new_name,
                'reason': p.reason,
                'priority': p.priority,
                'category': p.category,
                'confidence': p.confidence,
                'is_valid': p.is_valid_name()
            }
            for p in proposals
        ]
    }
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Rename plan exported to {output_file}")


def print_rename_report(proposals: List[RenameProposal]):
    """Print a formatted rename report."""
    print("\n" + "="*80)
    print("REPOSITORY RENAME PLAN")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Proposals: {len(proposals)}")
    print("="*80)
    print()
    
    # Group by priority
    by_priority = {'high': [], 'medium': [], 'low': []}
    for p in proposals:
        by_priority[p.priority].append(p)
    
    for priority in ['high', 'medium', 'low']:
        items = by_priority[priority]
        if not items:
            continue
        
        print(f"\n{priority.upper()} PRIORITY ({len(items)} repositories)")
        print("-" * 80)
        
        for p in items:
            print(f"\n{p.current_name}")
            print(f"  → {p.new_name}")
            print(f"  Reason: {p.reason}")
            print(f"  Category: {p.category}")
    
    print("\n" + "="*80)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Rename GitHub repositories with descriptive names using gh CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview all rename proposals
  python github_repo_renamer.py --username Notoriousjayy --preview
  
  # Export rename plan to JSON
  python github_repo_renamer.py --username Notoriousjayy --export rename_plan.json
  
  # Dry run (see what would be renamed)
  python github_repo_renamer.py --username Notoriousjayy --dry-run
  
  # Rename only high priority repositories
  python github_repo_renamer.py --username Notoriousjayy --priority high
  
  # Actually rename all repositories
  python github_repo_renamer.py --username Notoriousjayy --execute
  
  # Rename specific repositories
  python github_repo_renamer.py --username Notoriousjayy --repos Building-Microservices WASM --execute
        """
    )
    
    parser.add_argument(
        '--username',
        required=True,
        help='GitHub username'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview rename proposals without making changes'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate renames without making actual changes'
    )
    
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually execute the renames (WARNING: This makes real changes!)'
    )
    
    parser.add_argument(
        '--priority',
        choices=['high', 'medium', 'low'],
        help='Only rename repositories with this priority level'
    )
    
    parser.add_argument(
        '--repos',
        nargs='+',
        help='Specific repositories to rename'
    )
    
    parser.add_argument(
        '--export',
        help='Export rename plan to JSON file'
    )
    
    parser.add_argument(
        '--analysis',
        help='Path to analysis JSON file from repo description updater'
    )
    
    args = parser.parse_args()
    
    # Determine mode
    if not any([args.preview, args.dry_run, args.execute]):
        # Default to preview mode
        args.preview = True
    
    dry_run = not args.execute
    
    try:
        # Initialize renamer
        renamer = RepositoryRenamer(args.username, dry_run=dry_run)
        
        # Generate proposals
        logger.info("Generating rename proposals...")
        proposals = renamer.generate_rename_proposals(args.analysis)
        
        # Filter by specific repos if requested
        if args.repos:
            proposals = [p for p in proposals if p.current_name in args.repos]
            logger.info(f"Filtered to {len(proposals)} specific repositories")
        
        # Filter by priority if requested
        if args.priority:
            original_count = len(proposals)
            proposals = [p for p in proposals if p.priority == args.priority]
            logger.info(f"Filtered by priority '{args.priority}': {len(proposals)}/{original_count}")
        
        if not proposals:
            logger.warning("No repositories to rename based on current filters")
            return
        
        # Preview mode
        if args.preview:
            print_rename_report(proposals)
            return
        
        # Export mode
        if args.export:
            export_rename_plan(proposals, args.export)
        
        # Execute renames
        if args.dry_run or args.execute:
            logger.info(f"\n{'[DRY RUN] ' if dry_run else ''}Starting repository renames...")
            
            successful, failed = renamer.batch_rename(proposals, args.priority)
            
            logger.info(f"\nRename Summary:")
            logger.info(f"  Successful: {successful}")
            logger.info(f"  Failed: {failed}")
            logger.info(f"  Total: {len(proposals)}")
            
            if not dry_run:
                logger.info("\n⚠️  IMPORTANT: Update your local git remotes!")
                logger.info("For each renamed repository, run:")
                logger.info("  git remote set-url origin https://github.com/USERNAME/NEW-REPO-NAME.git")
        
        logger.info("\nComplete!")
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
