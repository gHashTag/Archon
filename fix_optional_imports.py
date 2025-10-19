#!/usr/bin/env python3
"""
Fix missing Optional imports in Python files.
Finds files using Optional[...] without importing Optional from typing.
"""

import re
from pathlib import Path

def has_optional_usage(content: str) -> bool:
    """Check if file uses Optional[...]"""
    return bool(re.search(r'\bOptional\[', content))

def has_optional_import(content: str) -> bool:
    """Check if file imports Optional from typing"""
    # Match various import patterns:
    # from typing import Optional
    # from typing import Dict, Optional
    # from typing import (Optional, ...)
    patterns = [
        r'from typing import.*\bOptional\b',
        r'from typing import.*\(.*\bOptional\b.*\)',
    ]
    return any(re.search(pattern, content) for pattern in patterns)

def add_optional_import(content: str) -> str:
    """Add Optional to existing typing import or create new one"""
    lines = content.split('\n')

    # Find existing 'from typing import' line
    for i, line in enumerate(lines):
        if line.strip().startswith('from typing import'):
            # Check if it's a single line or multiline import
            if '(' in line:
                # Multiline import - add Optional to the list
                # Find the closing paren
                j = i
                while j < len(lines) and ')' not in lines[j]:
                    j += 1
                # Add Optional before the closing paren
                if 'Optional' not in line and 'Optional' not in '\n'.join(lines[i:j+1]):
                    lines[j] = lines[j].replace(')', ', Optional)')
            else:
                # Single line import
                if 'Optional' not in line:
                    line = line.rstrip()
                    if line.endswith(','):
                        lines[i] = f"{line} Optional"
                    else:
                        lines[i] = f"{line}, Optional"
            return '\n'.join(lines)

    # No existing typing import found, add new one after other imports
    # Find the last import statement
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')):
            last_import_idx = i

    if last_import_idx >= 0:
        # Insert after last import
        lines.insert(last_import_idx + 1, 'from typing import Optional')
    else:
        # No imports found, add at the beginning (after shebang/docstring if any)
        insert_idx = 0
        if lines and lines[0].startswith('#!'):
            insert_idx = 1
        if insert_idx < len(lines) and (lines[insert_idx].strip().startswith('"""') or lines[insert_idx].strip().startswith("'''")):
            # Skip docstring
            while insert_idx < len(lines):
                insert_idx += 1
                if '"""' in lines[insert_idx] or "'''" in lines[insert_idx]:
                    insert_idx += 1
                    break
        lines.insert(insert_idx, 'from typing import Optional')

    return '\n'.join(lines)

def main():
    python_dir = Path('python/src')
    files_fixed = []
    files_checked = 0

    for py_file in python_dir.rglob('*.py'):
        files_checked += 1
        content = py_file.read_text(encoding='utf-8')

        if has_optional_usage(content) and not has_optional_import(content):
            print(f"❌ Missing Optional import: {py_file}")

            # Fix the import
            fixed_content = add_optional_import(content)
            py_file.write_text(fixed_content, encoding='utf-8')

            files_fixed.append(str(py_file))
            print(f"✅ Fixed: {py_file}")

    print(f"\n{'='*60}")
    print(f"📊 SUMMARY:")
    print(f"   Files checked: {files_checked}")
    print(f"   Files fixed: {len(files_fixed)}")
    print(f"{'='*60}")

    if files_fixed:
        print("\n✅ Fixed files:")
        for f in files_fixed:
            print(f"   - {f}")
    else:
        print("\n✅ All files already have correct Optional imports!")

if __name__ == '__main__':
    main()
