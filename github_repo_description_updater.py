#!/usr/bin/env python3
"""
GitHub Repository Description Updater
======================================
A comprehensive script that analyzes GitHub repositories and updates them with
appropriate descriptive names based on their content, structure, and purpose.

Author: Jordan Suber
Date: January 2026
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re

try:
    import requests
    from github import Github, GithubException, Repository
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install: pip install PyGithub requests")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('repo_description_update.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class RepositoryAnalysis:
    """Data class to hold repository analysis results."""
    name: str
    current_description: Optional[str]
    suggested_description: str
    primary_language: Optional[str]
    topics: List[str]
    has_readme: bool
    file_count: int
    confidence: float  # 0.0 to 1.0
    reasoning: str


class RepositoryDescriptionGenerator:
    """
    Generates appropriate descriptions for GitHub repositories based on
    content analysis, naming patterns, and common project structures.
    """
    
    # Predefined descriptions for known project types
    DESCRIPTION_PATTERNS = {
        # Syntax Diagram Projects
        r'c23.*syntax.*diagram': 'Interactive C23 language syntax diagrams with railroad visualizations and EBNF notation',
        r'javascript.*syntax.*diagram': 'Interactive JavaScript language syntax diagrams with railroad visualizations',
        r'python.*syntax.*diagram': 'Interactive Python language syntax diagrams with railroad visualizations',
        r'cpp23.*syntax.*diagram': 'Interactive C++23 language syntax diagrams with railroad visualizations and EBNF notation',
        r'java21.*syntax.*diagram': 'Interactive Java 21 language syntax diagrams with railroad visualizations',
        
        # GHAS/Security Projects
        r'ghas.*code.*scanning': 'GitHub Advanced Security (GHAS) code scanning toolkit with automation utilities and best practices',
        r'ghas.*toolkit': 'GitHub Advanced Security integration tools and automation utilities',
        
        # WebAssembly Projects
        r'wasm$': 'WebAssembly development projects and experiments with C/C++ compilation',
        r'webgl.*wasm.*pong': 'WebGL2 Pong game implementation using WebAssembly for high-performance rendering',
        
        # OpenGL Projects
        r'minimal.*moderngl': 'Minimal Modern OpenGL examples and learning resources with C++',
        r'opengl': 'OpenGL graphics programming projects and examples',
        
        # Infrastructure/DevOps Projects
        r'terraform.*aws': 'Terraform Infrastructure as Code (IaC) for AWS cloud resource management',
        r'moodle.*eks.*terraform': 'Terraform blueprint for deploying Moodle LMS on Amazon EKS',
        r'nginx.*web.*proxy': 'Nginx reverse proxy configuration and management utilities',
        r'terra.*dns.*stack': 'Terraform DNS infrastructure stack with Route53 integration',
        
        # React/Frontend Projects
        r'react.*streamline': 'Streamlined React application starter template with modern best practices',
        
        # Spring Projects
        r'spring.*streamline': 'Streamlined Spring Boot application template with enterprise patterns',
        
        # Utility Projects
        r'compiler.*contracts': 'Compiler design contract definitions and specifications',
        r'matrix.*element.*randomizer': 'Matrix manipulation utility for randomizing array elements',
        r'notification.*batch.*processor': 'Batch processing system for notification handling and delivery',
        
        # Cloud Computing
        r'cloud.*computing.*architecture.*mapping': 'Comprehensive cloud computing architecture book mapping and documentation',
        r'cloud.*computing.*mapping': 'Cloud computing concepts mapping and educational resources',
        
        # GitHub Skills/Training
        r'skills.*change.*commit': 'GitHub Skills course: Changing commit history with interactive exercises',
        r'skills.*introduction.*codeql': 'GitHub Skills course: Introduction to CodeQL security analysis',
        r'skills.*secret.*scanning': 'GitHub Skills course: Introduction to Secret Scanning',
        r'skills.*repository.*supply.*chain': 'GitHub Skills course: Securing repository supply chain',
        
        # Game Projects
        r'binaryville': 'Binary number learning game with interactive challenges',
        r'techteenspong': 'Educational Pong game implementation for teaching programming concepts',
    }
    
    def __init__(self, github_token: str):
        """Initialize the description generator with GitHub token."""
        self.github = Github(github_token)
        self.user = self.github.get_user()
        logger.info(f"Authenticated as: {self.user.login}")
    
    def analyze_repository(self, repo: Repository.Repository) -> RepositoryAnalysis:
        """
        Analyze a repository and generate an appropriate description.
        
        Args:
            repo: GitHub Repository object
            
        Returns:
            RepositoryAnalysis object with suggested description
        """
        logger.info(f"Analyzing repository: {repo.name}")
        
        # Gather repository information
        current_description = repo.description
        primary_language = repo.language
        topics = repo.get_topics()
        
        # Check for README
        has_readme = self._check_readme(repo)
        
        # Get file count (approximate)
        file_count = self._estimate_file_count(repo)
        
        # Generate description
        suggested_description, confidence, reasoning = self._generate_description(
            repo, has_readme, primary_language, topics
        )
        
        return RepositoryAnalysis(
            name=repo.name,
            current_description=current_description,
            suggested_description=suggested_description,
            primary_language=primary_language,
            topics=topics,
            has_readme=has_readme,
            file_count=file_count,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def _check_readme(self, repo: Repository.Repository) -> bool:
        """Check if repository has a README file."""
        try:
            repo.get_readme()
            return True
        except GithubException:
            return False
    
    def _estimate_file_count(self, repo: Repository.Repository) -> int:
        """Estimate the number of files in the repository."""
        try:
            contents = repo.get_contents("")
            return len(list(contents))
        except GithubException:
            return 0
    
    def _read_readme_content(self, repo: Repository.Repository) -> Optional[str]:
        """Read and return README content if available."""
        try:
            readme = repo.get_readme()
            content = readme.decoded_content.decode('utf-8')
            return content
        except GithubException:
            return None
    
    def _generate_description(
        self, 
        repo: Repository.Repository,
        has_readme: bool,
        primary_language: Optional[str],
        topics: List[str]
    ) -> Tuple[str, float, str]:
        """
        Generate a description for the repository.
        
        Returns:
            Tuple of (description, confidence, reasoning)
        """
        repo_name_lower = repo.name.lower()
        
        # Step 1: Check against predefined patterns
        for pattern, description in self.DESCRIPTION_PATTERNS.items():
            if re.search(pattern, repo_name_lower):
                return (
                    description,
                    0.95,
                    f"Matched pattern: {pattern}"
                )
        
        # Step 2: Analyze README if available
        if has_readme:
            readme_content = self._read_readme_content(repo)
            if readme_content:
                readme_based_desc = self._extract_description_from_readme(readme_content)
                if readme_based_desc:
                    return (
                        readme_based_desc,
                        0.85,
                        "Extracted from README content"
                    )
        
        # Step 3: Generate from language and topics
        if primary_language or topics:
            generated_desc = self._generate_from_metadata(
                repo_name_lower, primary_language, topics
            )
            if generated_desc:
                return (
                    generated_desc,
                    0.70,
                    "Generated from language and topics"
                )
        
        # Step 4: Generate generic description from name
        generic_desc = self._generate_generic_description(repo.name)
        return (
            generic_desc,
            0.50,
            "Generic description from repository name"
        )
    
    def _extract_description_from_readme(self, readme: str) -> Optional[str]:
        """Extract a suitable description from README content."""
        lines = readme.split('\n')
        
        # Look for the first non-header, non-empty line with substantial content
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip headers, empty lines, and badges
            if not line or line.startswith('#') or '[![' in line or line.startswith('!['):
                continue
            
            # Skip lines that are just links or code blocks
            if line.startswith('[') or line.startswith('```') or line.startswith('---'):
                continue
            
            # Found a potential description
            if len(line) > 20 and len(line) < 200:
                # Clean up the description
                clean_desc = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)  # Remove markdown links
                clean_desc = re.sub(r'[*_`]', '', clean_desc)  # Remove markdown formatting
                clean_desc = clean_desc.strip()
                
                if clean_desc and not clean_desc.startswith('http'):
                    return clean_desc
        
        return None
    
    def _generate_from_metadata(
        self, 
        repo_name: str, 
        language: Optional[str], 
        topics: List[str]
    ) -> Optional[str]:
        """Generate description from repository metadata."""
        parts = []
        
        # Add language context
        if language:
            parts.append(f"{language}-based")
        
        # Add topic context
        if topics:
            relevant_topics = [t for t in topics if t not in ['github', 'repo', 'repository']]
            if relevant_topics:
                parts.append(', '.join(relevant_topics[:3]))
        
        # Parse repository name for hints
        name_parts = re.split(r'[-_]', repo_name)
        significant_parts = [p for p in name_parts if len(p) > 3]
        
        if parts:
            base = ' '.join(parts)
            return f"{base} project implementing {' '.join(significant_parts[:2])}"
        
        return None
    
    def _generate_generic_description(self, repo_name: str) -> str:
        """Generate a generic but meaningful description from the repository name."""
        # Convert camelCase and kebab-case to words
        words = re.sub(r'([A-Z])', r' \1', repo_name)
        words = words.replace('-', ' ').replace('_', ' ')
        words = ' '.join(words.split())
        
        return f"{words} - Software development project"


class RepositoryUpdater:
    """Handles updating repository descriptions on GitHub."""
    
    def __init__(self, github_token: str, dry_run: bool = False):
        """
        Initialize the repository updater.
        
        Args:
            github_token: GitHub personal access token
            dry_run: If True, only simulate updates without making changes
        """
        self.github = Github(github_token)
        self.user = self.github.get_user()
        self.dry_run = dry_run
        logger.info(f"Repository Updater initialized (dry_run={dry_run})")
    
    def update_repository_description(
        self, 
        repo: Repository.Repository, 
        new_description: str
    ) -> bool:
        """
        Update a repository's description.
        
        Args:
            repo: GitHub Repository object
            new_description: New description to set
            
        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            logger.info(f"[DRY RUN] Would update {repo.name}: '{new_description}'")
            return True
        
        try:
            repo.edit(description=new_description)
            logger.info(f"✓ Updated {repo.name}: '{new_description}'")
            return True
        except GithubException as e:
            logger.error(f"✗ Failed to update {repo.name}: {str(e)}")
            return False


def format_analysis_report(analyses: List[RepositoryAnalysis]) -> str:
    """Format analysis results into a readable report."""
    report = []
    report.append("=" * 80)
    report.append("REPOSITORY DESCRIPTION ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Repositories Analyzed: {len(analyses)}")
    report.append("=" * 80)
    report.append("")
    
    for i, analysis in enumerate(analyses, 1):
        report.append(f"{i}. {analysis.name}")
        report.append("-" * 80)
        
        if analysis.current_description:
            report.append(f"   Current:  {analysis.current_description}")
        else:
            report.append(f"   Current:  (empty)")
        
        report.append(f"   Suggested: {analysis.suggested_description}")
        report.append(f"   Language:  {analysis.primary_language or 'N/A'}")
        report.append(f"   Confidence: {analysis.confidence:.0%}")
        report.append(f"   Reasoning: {analysis.reasoning}")
        
        if analysis.topics:
            report.append(f"   Topics: {', '.join(analysis.topics)}")
        
        report.append("")
    
    report.append("=" * 80)
    return "\n".join(report)


def save_analysis_json(analyses: List[RepositoryAnalysis], output_file: str):
    """Save analysis results to JSON file."""
    data = {
        'generated_at': datetime.now().isoformat(),
        'total_repositories': len(analyses),
        'analyses': [
            {
                'name': a.name,
                'current_description': a.current_description,
                'suggested_description': a.suggested_description,
                'primary_language': a.primary_language,
                'topics': a.topics,
                'has_readme': a.has_readme,
                'file_count': a.file_count,
                'confidence': a.confidence,
                'reasoning': a.reasoning
            }
            for a in analyses
        ]
    }
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Analysis saved to {output_file}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Analyze and update GitHub repository descriptions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all repositories and show suggestions
  python github_repo_description_updater.py --token YOUR_TOKEN --analyze
  
  # Update all repositories with suggested descriptions
  python github_repo_description_updater.py --token YOUR_TOKEN --update-all
  
  # Dry run to see what would be updated
  python github_repo_description_updater.py --token YOUR_TOKEN --update-all --dry-run
  
  # Update specific repositories
  python github_repo_description_updater.py --token YOUR_TOKEN --repos repo1 repo2 --update
  
  # Export analysis to JSON
  python github_repo_description_updater.py --token YOUR_TOKEN --analyze --export analysis.json
        """
    )
    
    parser.add_argument(
        '--token',
        required=False,
        help='GitHub personal access token (or set GITHUB_TOKEN env var)'
    )
    
    parser.add_argument(
        '--username',
        help='GitHub username (defaults to authenticated user)'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze repositories and show suggestions'
    )
    
    parser.add_argument(
        '--update-all',
        action='store_true',
        help='Update all repositories with suggested descriptions'
    )
    
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update specified repositories (use with --repos)'
    )
    
    parser.add_argument(
        '--repos',
        nargs='+',
        help='List of repository names to process'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate updates without making changes'
    )
    
    parser.add_argument(
        '--export',
        help='Export analysis to JSON file'
    )
    
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.0,
        help='Minimum confidence threshold for updates (0.0-1.0)'
    )
    
    parser.add_argument(
        '--skip-empty',
        action='store_true',
        help='Skip repositories that already have descriptions'
    )
    
    args = parser.parse_args()
    
    # Get GitHub token
    github_token = args.token or os.environ.get('GITHUB_TOKEN')
    if not github_token:
        logger.error("Error: GitHub token required. Use --token or set GITHUB_TOKEN environment variable")
        sys.exit(1)
    
    try:
        # Initialize components
        generator = RepositoryDescriptionGenerator(github_token)
        updater = RepositoryUpdater(github_token, dry_run=args.dry_run)
        
        # Get repositories to process
        username = args.username or generator.user.login
        user = generator.github.get_user(username)
        
        if args.repos:
            repos_to_process = []
            for repo_name in args.repos:
                try:
                    repo = user.get_repo(repo_name)
                    repos_to_process.append(repo)
                except GithubException:
                    logger.warning(f"Repository not found: {repo_name}")
        else:
            repos_to_process = list(user.get_repos())
        
        logger.info(f"Processing {len(repos_to_process)} repositories...")
        
        # Analyze repositories
        analyses = []
        for repo in repos_to_process:
            try:
                analysis = generator.analyze_repository(repo)
                analyses.append(analysis)
            except Exception as e:
                logger.error(f"Error analyzing {repo.name}: {str(e)}")
        
        # Generate report
        report = format_analysis_report(analyses)
        print("\n" + report)
        
        # Export to JSON if requested
        if args.export:
            save_analysis_json(analyses, args.export)
        
        # Update repositories if requested
        if args.update_all or args.update:
            logger.info("\nUpdating repository descriptions...")
            
            updated = 0
            skipped = 0
            
            for analysis in analyses:
                # Skip if confidence is too low
                if analysis.confidence < args.min_confidence:
                    logger.info(f"Skipping {analysis.name} (confidence {analysis.confidence:.0%} < {args.min_confidence:.0%})")
                    skipped += 1
                    continue
                
                # Skip if already has description and --skip-empty is set
                if args.skip_empty and analysis.current_description:
                    logger.info(f"Skipping {analysis.name} (already has description)")
                    skipped += 1
                    continue
                
                # Get the repository object
                repo = user.get_repo(analysis.name)
                
                # Update the description
                if updater.update_repository_description(repo, analysis.suggested_description):
                    updated += 1
            
            logger.info(f"\nUpdate Summary: {updated} updated, {skipped} skipped")
        
        logger.info("\nComplete!")
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
