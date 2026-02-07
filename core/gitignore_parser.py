"""
.gitignore Parser - Parse and process gitignore patterns
"""

import re
from pathlib import Path
from typing import List

class GitIgnoreParser:
    """Parse and handle .gitignore files"""
    
    @staticmethod
    def parse_gitignore(gitignore_path: Path) -> List[str]:
        """Parse .gitignore file and extract patterns"""
        patterns = []
        
        if not gitignore_path.exists():
            return patterns
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except Exception as e:
            print(f"Error parsing gitignore: {e}")
        
        return patterns
    
    @staticmethod
    def should_ignore(path: str, patterns: List[str]) -> bool:
        """Check if path matches any gitignore pattern"""
        path_obj = Path(path)
        
        for pattern in patterns:
            # Handle directory patterns (ending with /)
            if pattern.endswith('/'):
                if path_obj.name == pattern[:-1]:
                    return True
            
            # Handle wildcard patterns
            elif pattern.endswith('*'):
                prefix = pattern[:-1]
                if path_obj.name.startswith(prefix):
                    return True
            
            # Handle exact name matches
            elif path_obj.name == pattern:
                return True
            
            # Handle file extension patterns
            elif pattern.startswith('*.'):
                extension = pattern[1:]
                if path_obj.suffix == extension:
                    return True
        
        return False
    
    @staticmethod
    def create_default_patterns() -> List[str]:
        """Create default ignore patterns if no .gitignore exists"""
        return [
            '.git',
            '.gitignore',
            'node_modules',
            'venv',
            '.venv',
            '__pycache__',
            'dist',
            'build',
            '.pytest_cache',
            '*.pyc',
            '*.log',
            '.DS_Store',
            'Thumbs.db',
        ]