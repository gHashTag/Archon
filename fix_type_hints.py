#!/usr/bin/env python3
"""
Fix Python 3.10+ union type syntax (Type | None) to Python 3.9 compatible Optional[Type]
"""
import re
import sys
from pathlib import Path

def fix_type_hints(file_path):
    """Fix union type hints in a single file."""
    with open(file_path, 'r') as f:
        content = f.read()

    original = content

    # Pattern to match Type | None in various contexts
    # Handles: dict[str, Any] | None, list[str] | None, SomeType | None, etc.
    pattern = r'([:\->])\s*([A-Za-z_][A-Za-z0-9_\[\],\s]*?)\s+\|\s+None'

    def replace_union(match):
        prefix = match.group(1)
        type_part = match.group(2).strip()
        return f'{prefix} Optional[{type_part}]'

    content = re.sub(pattern, replace_union, content)

    # Check if we need to add Optional import
    has_optional = 'from typing import' in content and 'Optional' in content
    needs_optional = 'Optional[' in content

    if needs_optional and not has_optional:
        # Add Optional to existing typing import
        if 'from typing import' in content:
            content = re.sub(
                r'(from typing import [^\n]+)',
                lambda m: m.group(1) + ', Optional' if 'Optional' not in m.group(1) else m.group(1),
                content,
                count=1
            )
        else:
            # Add new typing import at the top after docstring
            lines = content.split('\n')
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('"""') and not line.strip().startswith("'''"):
                    insert_pos = i
                    break
            lines.insert(insert_pos, 'from typing import Optional')
            content = '\n'.join(lines)

    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    src_path = Path('.')
    fixed_count = 0

    for py_file in src_path.rglob('*.py'):
        if fix_type_hints(py_file):
            print(f'Fixed: {py_file}')
            fixed_count += 1

    print(f'\nTotal files fixed: {fixed_count}')

if __name__ == '__main__':
    main()
