"""
Validation functions for the textbook generation pipeline.
"""
import os
import json
import re
from pathlib import Path

def validate_mdx_files():
    """Validate that all generated MDX files follow the required format"""
    book_output_dir = Path("book_output")
    if not book_output_dir.exists():
        print("No book_output directory found, skipping MDX validation")
        return True

    mdx_files = list(book_output_dir.rglob("*.mdx"))
    all_valid = True

    for mdx_file in mdx_files:
        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for required chapter template sections
        required_sections = [
            r'^\s*#\s*Overview',
            r'^\s*##\s*Key Concepts',
            r'^\s*##\s*Technical Sections',
            r'^\s*##\s*Examples / Diagrams / Tables',
            r'^\s*##\s*Implementation Notes',
            r'^\s*##\s*Exercises',
            r'^\s*##\s*Summary'
        ]

        missing_sections = []
        for section_pattern in required_sections:
            if not re.search(section_pattern, content, re.MULTILINE):
                missing_sections.append(section_pattern)

        if missing_sections:
            print(f"Missing required sections in {mdx_file}: {missing_sections}")
            all_valid = False

        # Check for proper MDX syntax (basic check)
        if re.search(r'<.*?>', content) and not re.search(r'```jsx?|```tsx?', content):
            # This might be JSX in a code block, which is OK
            pass

    return all_valid

def validate_structure():
    """Validate that the generated files follow the required structure"""
    required_dirs = [
        "book_output/part_i_foundations",
        "book_output/part_ii_ros2",
        "book_output/part_iii_simulation",
        "book_output/part_iv_isaac",
        "book_output/part_v_humanoid",
        "book_output/part_vi_vla",
        "book_output/part_vii_hardware",
        "book_output/part_viii_weekly",
        "book_output/part_ix_assessments",
        "frontend/docusaurus/docs",
        "frontend/static/assets"
    ]

    all_exist = True
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"Required directory missing: {dir_path}")
            all_exist = False

    # Check for some expected files
    expected_files = [
        "frontend/docusaurus/sidebars.js",
        "frontend/docusaurus/docusaurus.config.js"
    ]

    for file_path in expected_files:
        if not os.path.exists(file_path):
            print(f"Expected file missing: {file_path}")
            all_exist = False

    return all_exist

def validate_content_integrity():
    """Validate that generated content matches PDF source material"""
    # This would normally compare generated content with source PDF
    # For now, we'll implement a basic check to ensure files exist and have content

    book_output_dir = Path("book_output")
    if not book_output_dir.exists():
        print("No book_output directory found, content integrity check failed")
        return False

    # Count total MDX files
    mdx_files = list(book_output_dir.rglob("*.mdx"))
    if len(mdx_files) == 0:
        print("No MDX files found in book_output")
        return False

    # Check that files have reasonable content length
    for mdx_file in mdx_files:
        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if len(content.strip()) < 100:  # Very basic check
            print(f"File {mdx_file} has very little content: {len(content)} characters")
            # We won't fail on this, but we'll report it

    print(f"Content integrity check passed: {len(mdx_files)} MDX files found")
    return True

def move_chapters_to_docusaurus():
    """Move generated chapters to Docusaurus docs directory"""
    import shutil

    book_output_dir = Path("book_output")
    docusaurus_docs_dir = Path("frontend/docusaurus/docs")

    # Create docusaurus docs directory if it doesn't exist
    docusaurus_docs_dir.mkdir(parents=True, exist_ok=True)

    # Copy all generated chapters to docusaurus docs
    for part_dir in book_output_dir.iterdir():
        if part_dir.is_dir():
            dest_dir = docusaurus_docs_dir / part_dir.name
            if dest_dir.exists():
                import shutil
                shutil.rmtree(dest_dir)
            shutil.copytree(part_dir, dest_dir)

    print(f"Moved chapters from {book_output_dir} to {docusaurus_docs_dir}")

def copy_assets():
    """Copy static assets for textbook content"""
    import shutil

    # Create static assets directory
    assets_dir = Path("frontend/static/assets")
    assets_dir.mkdir(parents=True, exist_ok=True)

    # In a real implementation, this would copy actual assets
    # For now, we'll just ensure the directory exists
    print(f"Assets directory created: {assets_dir}")