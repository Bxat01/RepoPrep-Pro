"""
.gitignore Parser
"""

import re
from pathlib import Path
from typing import List

class GitIgnoreParser:
    """Simple .gitignore parser"""
    
    @staticmethod
    def parse_gitignore(gitignore_path: Path) -> List[str]:
        """Parse .gitignore file"""
        patterns = []
        
        if not gitignore_path.exists():
            return patterns
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except:
            pass
        
        return patterns
    
    @staticmethod
    def should_ignore(path: str, patterns: List[str]) -> bool:
        """Check if path matches any pattern"""
        from pathlib import Path
        path_obj = Path(path)
        
        for pattern in patterns:
            # Simple pattern matching
            if pattern.endswith('/'):
                if path_obj.name == pattern[:-1]:
                    return True
            elif pattern.endswith('*'):
                prefix = pattern[:-1]
                if path_obj.name.startswith(prefix):
                    return True
            elif path_obj.name == pattern:
                return True
        
        return False