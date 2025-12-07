---
id: 2
title: Create Physical AI Textbook Spec
stage: spec
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-textbook
branch: 001-physical-ai-textbook
user: User
command: /sp.specify
labels: [spec, physical-ai, textbook, docusaurus, robotics]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-physical-ai-textbook/spec.md
 - specs/001-physical-ai-textbook/checklists/requirements.md
 - history/prompts/001-physical-ai-textbook/
tests:
 - none
---

## Prompt

```text
SYSTEM PURPOSE:
Define the complete Spec-Kit-Plus project specification for generating a Docusaurus-based textbook derived solely from the Physical AI & Humanoid Robotics PDF. This specification governs the project's goals, inputs, outputs, constraints, folder structure, agents, files, pipelines, and generation expectations.

1. PROJECT SUMMARY

You will generate a full technical textbook and deployed Docusaurus documentation site based exclusively on the Physical AI & Humanoid Robotics textbook PDF. All content, outlines, and chapters must reflect the themes and course architecture defined in the PDF, including:

Physical AI & Embodied Intelligence

ROS 2 (nodes, topics, services, actions, URDF)

Gazebo & Unity Simulation

NVIDIA Isaac Sim / Isaac ROS / Navigation

VLA (Vision-Language-Action)

Humanoid Kinematics, Dynamics, Locomotion

Weekly curriculum structure (Weeks 1–13)

Hardware requirements and lab architectures

Assessments and capstone

Budget vs premium hardware pathways

The entire project must be reproducible, modular, and ready for multi-agent orchestration (Claude Code + Qwen Code API).

2. CORE GOALS

Convert the PDF into a clean, hierarchical book specification.

Translate all content into chapter-ready structures for Qwen Code generation.

Produce Docusaurus-compatible markdown and sidebar structures.

Build reusable pipelines for chapter extraction, generation, and revision.

Ensure the project complies with the required folder structure.

Enable future integration of:

RAG chatbot

personalization

translation features

3. SCOPE & BOUNDARIES
3.1 In-Scope

Book outline and chapter specification

Processing logic for extracting PDF themes

Qwen Code generation prompts per chapter

Claude Code orchestrator instructions

Docusaurus configuration structure

Markdown formatting rules

Bibliography, assessments, hardware tables

3.2 Out-of-Scope

Any topic or content not found in the PDF

Any robotics framework not included in PDF (e.g., ROS1, Mujoco, MoveIt)

Unverified or fictional humanoid systems

Tutorial-style coding walkthroughs beyond textbook scope

4. PRODUCED ARTIFACTS

The system must ultimately produce:

Book Specification

global outline

chapter list

hierarchical section structure

mapping of text to Qwen generation tasks

Generation Pipelines

extraction pipeline (PDF → topics)

chapter generation pipeline (Qwen)

orchestration pipeline (Claude Code)

Frontend Integration

Docusaurus sidebar.js

MDX chapters

static assets placement

Backend Integration

Qwen API wrappers

orchestrator logic

utils for formatting/validation

Book Output

fully generated markdown chapters

ready-to-publish Docusaurus site

5. REQUIRED FOLDER STRUCTURE

All specifications, pipelines, and generation outputs must conform to:

project-root/
├── backend/
│   ├── qwen/
│   ├── pipelines/
│   ├── processing/
│   ├── orchestrator/
│   └── utils/
├── frontend/
│   ├── docusaurus/
│   ├── src/
│   ├── static/
│   └── theme/
└── book_output/


No deviations permitted.

6. AGENT ROLES
6.1 Claude Code (Orchestrator)

Responsible for:

running pipelines

feeding chapter specs to Qwen

validating outputs

assembling Docusaurus files

producing final book folder

6.2 Qwen Code API (Generator)

Responsible for:

writing chapter content

following strict formatting + style rules

outputting deterministic MDX content

maintaining technical accuracy from the PDF

6.3 Spec-Kit-Plus (This File)

Defines:

project requirements

constraints

roles

pipelines

artifacts

operational rules

7. PIPELINE REQUIREMENTS
7.1 PDF Processing Pipeline

Extract top-level themes.

Extract module structure.

Extract weekly breakdown.

Extract hardware details.

Produce structured JSON representing the course.

7.2 Book Generation Pipeline

Convert extracted JSON → chapter specifications.

Validate chapter hierarchy.

Produce deterministic chapter prompts for Qwen.

Assemble markdown outputs.

7.3 Assembly Pipeline

Generate sidebar definitions.

Ge
```

## Response snapshot

Created a comprehensive specification for the Physical AI & Humanoid Robotics textbook project. The spec defines user scenarios for generating a complete Docusaurus-based textbook from the source PDF, extracting content about Physical AI, ROS 2, NVIDIA Isaac, simulation systems, and hardware requirements. The specification includes functional requirements for processing the 13-week curriculum, generating proper navigation, and maintaining technical accuracy from the source material.

## Outcome

- ✅ Impact: Created complete specification for Physical AI textbook generation project
- 🧪 Tests: none
- 📁 Files: Created spec.md and requirements checklist in specs/001-physical-ai-textbook/
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification covers all required content areas from the PDF with clear user scenarios and measurable outcomes

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all validation items passed
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): proceed with /sp.plan to create implementation plan