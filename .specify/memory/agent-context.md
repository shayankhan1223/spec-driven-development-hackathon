# Physical AI & Humanoid Robotics Textbook Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-07

## Active Technologies

- Python 3.11 for processing pipelines
- JavaScript/TypeScript for Docusaurus frontend
- Qwen Code API for content generation
- Claude Code orchestrator for workflow management
- Docusaurus v3 for documentation site
- PDF processing libraries (PyPDF2/PyMuPDF)
- ROS 2 tools and frameworks
- NVIDIA Isaac libraries
- pytest for backend testing
- Jest for frontend testing

## Project Structure

```text
project-root/
├── backend/
│   ├── qwen/
│   │   ├── api_client.py
│   │   └── generation.py
│   ├── pipelines/
│   │   ├── pdf_extraction.py
│   │   ├── content_processing.py
│   │   └── chapter_generation.py
│   ├── processing/
│   │   ├── pdf_parser.py
│   │   ├── content_cleaner.py
│   │   └── json_formatter.py
│   ├── orchestrator/
│   │   ├── main.py
│   │   ├── task_manager.py
│   │   └── validation.py
│   └── utils/
│       ├── file_operations.py
│       ├── logger.py
│       └── config.py
├── frontend/
│   ├── docusaurus/
│   │   ├── docusaurus.config.js
│   │   ├── sidebar.js
│   │   └── src/
│   ├── src/
│   ├── static/
│   └── theme/
└── book_output/
    ├── part_i_foundations/
    ├── part_ii_ros2/
    ├── part_iii_simulation/
    ├── part_iv_isaac/
    ├── part_v_humanoid/
    ├── part_vi_vla/
    ├── part_vii_hardware/
    ├── part_viii_weekly/
    └── part_ix_assessments/
```

## Commands

# Generate Complete Textbook
python -m orchestrator.main --full-generation

# Generate Specific Part
python -m orchestrator.main --part "Part I -- Foundations of Physical AI"

# Validate Generated Content
python -m orchestrator.validation --check-content-accuracy

# Build Docusaurus Site
cd frontend/docusaurus && npm run build

# Serve Docusaurus Site Locally
cd frontend/docusaurus && npm run serve

## Code Style

- Python: Follow PEP 8 guidelines with 4-space indentation
- JavaScript: Use 2-space indentation, camelCase for variables
- Markdown: Use 2-space indentation for lists, consistent heading hierarchy
- File naming: Use snake_case for Python files, kebab-case for markdown files
- Imports: Group standard library, third-party, and local imports separately

## Recent Changes

- Feature 001-physical-ai-textbook: Added PDF processing pipeline to transform Physical AI textbook into Docusaurus-based chapters
- Created 9-part structure with 40+ chapters covering Physical AI, ROS 2, NVIDIA Isaac, simulation, and humanoid robotics
- Implemented multi-agent architecture with Claude Code orchestrator and Qwen Code generator

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->