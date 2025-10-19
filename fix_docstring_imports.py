#!/usr/bin/env python3
"""
Fix imports that were incorrectly placed inside docstrings.
"""

from pathlib import Path
import re

def fix_file(file_path: Path) -> bool:
    """Fix a single file if it has the pattern."""
    content = file_path.read_text(encoding='utf-8')

    # Pattern: docstring starts, then import on next line
    pattern = r'^"""\s*\nfrom typing import Optional\s*\n'

    if re.search(pattern, content, re.MULTILINE):
        # Find the docstring and move the import after it
        lines = content.split('\n')

        # Find closing """ of the opening docstring
        in_docstring = False
        docstring_end = -1

        for i, line in enumerate(lines):
            if i == 0 and line.strip() == '"""':
                in_docstring = True
                continue

            if in_docstring:
                if line.strip().startswith('from typing import Optional'):
                    # Remove this line
                    lines.pop(i)
                    # Continue to find the closing """
                    continue

                if '"""' in line:
                    docstring_end = i
                    break

        if docstring_end > 0:
            # Insert the import after the docstring
            lines.insert(docstring_end + 1, '')
            lines.insert(docstring_end + 2, 'from typing import Optional')

            file_path.write_text('\n'.join(lines), encoding='utf-8')
            return True

    return False

def main():
    python_dir = Path('python/src')
    fixed_count = 0

    for py_file in python_dir.rglob('*.py'):
        if fix_file(py_file):
            print(f"✅ Fixed: {py_file}")
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"📊 Fixed {fixed_count} files with imports inside docstrings")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
