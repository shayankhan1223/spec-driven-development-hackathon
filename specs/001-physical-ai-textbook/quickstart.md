# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook
**Date**: 2025-12-07
**Status**: Complete

## Overview

This guide provides a quick introduction to setting up and running the Physical AI & Humanoid Robotics textbook generation system. The system uses Claude Code and Qwen Code agents to transform a PDF into a complete Docusaurus-based textbook.

## Prerequisites

Before starting, ensure you have:

1. **Python 3.11+** installed on your system
2. **Node.js 18+** for Docusaurus frontend
3. **Access to Qwen Code API** with valid credentials
4. **Source PDF**: Physical AI & Humanoid Robotics textbook
5. **Git** for version control

## Setup

### 1. Clone and Initialize Repository

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies
cd frontend/docusaurus
npm install
```

### 2. Configure Environment

Create a `.env` file in the repository root:

```env
# Qwen Code API Configuration
QWEN_API_KEY=your_qwen_api_key
QWEN_API_ENDPOINT=https://api.qwen.com/v1

# Claude Code Configuration (if applicable)
CLAUDE_API_KEY=your_claude_api_key

# Processing Configuration
PDF_SOURCE_PATH=path/to/physical_ai_textbook.pdf
OUTPUT_PATH=book_output/
TEMP_PATH=temp/

# Docusaurus Configuration
DOCUSAURUS_BASE_URL=/
DOCUSAURUS_PORT=3000
```

### 3. Run the Generation Pipeline

```bash
# Navigate to backend
cd backend

# Run the complete pipeline
python orchestrator/main.py --pdf-path ../path/to/physical_ai_textbook.pdf --output-dir ../book_output

# Or run individual pipeline stages:
# 1. PDF Extraction
python pipelines/pdf_extraction.py --pdf-path ../path/to/physical_ai_textbook.pdf

# 2. Content Processing
python processing/content_processing.py

# 3. Chapter Generation (via Qwen Code)
python qwen/generation.py
```

## Project Structure

```
project-root/
├── backend/                 # Processing pipelines and orchestrator
│   ├── qwen/              # Qwen Code API integration
│   ├── pipelines/         # PDF extraction and processing
│   ├── processing/        # Content normalization
│   ├── orchestrator/      # Task management and validation
│   └── utils/             # Utility functions
├── frontend/              # Docusaurus documentation site
│   └── docusaurus/        # Docusaurus configuration and source
├── book_output/           # Generated textbook content
└── specs/                 # Feature specifications and plans
    └── 001-physical-ai-textbook/
        ├── spec.md        # Feature specification
        ├── plan.md        # Implementation plan
        ├── research.md    # Research and decisions
        ├── data-model.md  # Data models
        ├── quickstart.md  # This file
        └── contracts/     # API contracts
```

## Key Commands

### Generate Complete Textbook
```bash
cd backend
python -m orchestrator.main --full-generation
```

### Generate Specific Part
```bash
cd backend
python -m orchestrator.main --part "Part I -- Foundations of Physical AI"
```

### Validate Generated Content
```bash
cd backend
python -m orchestrator.validation --check-content-accuracy
```

### Build Docusaurus Site
```bash
cd frontend/docusaurus
npm run build
```

### Serve Docusaurus Site Locally
```bash
cd frontend/docusaurus
npm run serve
```

## Generated Content Structure

The system generates 9 parts with 40+ chapters:

```
book_output/
├── part_i_foundations/           # Foundations of Physical AI
│   ├── introduction_to_physical_ai.md
│   ├── embodied_intelligence.md
│   ├── why_physical_ai_matters.md
│   └── humanoid_robotics_landscape.md
├── part_ii_ros2/                # ROS 2: The Robotic Nervous System
│   ├── ros2_architecture.md
│   ├── nodes_topics_services.md
│   ├── ros2_packages_workflows.md
│   ├── urdf_humanoid_robots.md
│   └── launch_files_management.md
├── part_iii_simulation/         # Simulation: Gazebo & Unity Digital Twins
├── part_iv_isaac/               # NVIDIA Isaac AI Robotics Platform
├── part_v_humanoid/             # Humanoid Robotics Engineering
├── part_vi_vla/                 # Vision-Language-Action Systems
├── part_vii_hardware/           # Hardware, Labs & Infrastructure
├── part_viii_weekly/            # Weekly Learning Path (Weeks 1-13)
└── part_ix_assessments/         # Assessments & Capstone Project
```

## Configuration Options

### Processing Configuration
- `--max-workers`: Number of parallel processing workers (default: 4)
- `--chunk-size`: Size of content chunks for processing (default: 1000 words)
- `--validation-level`: Strictness of content validation (low, medium, high)

### Generation Configuration
- `--temperature`: Creativity level for content generation (0.0-1.0)
- `--max-tokens`: Maximum tokens per chapter (default: 4000)
- `--model`: Qwen model to use (default: qwen-max)

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify API keys are correctly set in `.env`
   - Check network connectivity to API endpoints

2. **PDF Processing Failures**
   - Ensure PDF is not password-protected
   - Verify PDF contains extractable text (not just images)

3. **Memory Issues**
   - Reduce `--max-workers` parameter
   - Process PDF in smaller chunks

4. **Content Quality Issues**
   - Adjust `--temperature` parameter
   - Verify source PDF quality

### Getting Help

- Check the [research.md](./research.md) for detailed implementation decisions
- Review the [data-model.md](./data-model.md) for entity relationships
- Consult the [plan.md](./plan.md) for architectural details