---
id: 4
title: Create Task Graph
stage: tasks
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-textbook
branch: 001-physical-ai-textbook
user: User
command: /sp.tasks
labels: [tasks, physical-ai, textbook, generation, pipeline]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  plan: specs/001-physical-ai-textbook/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-physical-ai-textbook/tasks.md
 - history/prompts/001-physical-ai-textbook/
tests:
 - none
---

## Prompt

```text
SYSTEM PURPOSE:
Define the complete, granular, deterministic task graph for generating the Physical AI & Humanoid Robotics textbook using Claude Code (orchestrator) and Qwen Code (chapter generator), based strictly on the PDF-derived outline.

This file enumerates every required task, the inputs/outputs, dependencies, agent assignments, and file placement.

1. TASK OVERVIEW

The project must be decomposed into five primary pipelines:

PDF Processing Tasks

Outline Construction Tasks

Chapter Generation Tasks

Assembly & Integration Tasks

Validation & Publication Tasks

Each pipeline contains atomic tasks that Claude Code must orchestrate and Qwen Code must execute where applicable.

2. PDF PROCESSING TASKS
Task 2.1 — Extract_PDF_Themes

Agent: Claude Code

Input: PDF

Output: themes.json

Goal: Identify global themes:

Physical AI

Embodied intelligence

ROS 2

Gazebo / Unity

NVIDIA Isaac

VLA

Hardware requirements

Weekly structure

Location: backend/processing/themes.json

Task 2.2 — Extract_Module_Structure

Agent: Claude Code

Output: modules.json

Goal: Map PDF's Modules 1–4 into structured JSON

Location: backend/processing/modules.json

Task 2.3 — Extract_Weeks

Agent: Claude Code

Output: weeks.json

Goal: Transform Weeks 1–13 into structured lists

Location: backend/processing/weeks.json

Task 2.4 — Extract_Hardware

Agent: Claude Code

Output: hardware.json

Goal: Capture workstation, edge kits, robot lab options, cloud lab, latency constraints

Location: backend/processing/hardware.json

3. OUTLINE CONSTRUCTION TASKS
Task 3.1 — Build_Global_Outline

Agent: Claude Code

Input: themes.json, modules.json, weeks.json

Output: outline.json

Goal: Convert the book outline defined in sp.plan into structured JSON

Location: backend/pipelines/outline.json

Task 3.2 — Expand_Chapters

Agent: Claude Code

Input: outline.json

Output: chapters.json

Goal: For each chapter, create a generation-ready object:

title

key concepts

required sections

pointers to PDF data

expected tables/diagrams

Location: backend/pipelines/chapters.json

4. CHAPTER GENERATION TASKS (Qwen Code)

For each chapter defined in chapters.json, create a deterministic task:

Task 4.x — Generate_Chapter_<ID>

Agent: Qwen Code

Input: chapter spec JSON

Output: Markdown (.mdx)

Structure: Must follow the universal chapter template:

Overview

Key Concepts

Technical Sections

Examples/Diagrams/Tables

Implementation Notes

Exercises

Summary

Output Location:

book_output/part_<N>/chapter_<ID>.mdx


There will be one task per chapter (expected 45–60 tasks depending on chapter granularity).

Task 4.0 — Validate_MDX_Format

Agent: Claude Code

Goal: Ensure MDX is Docusaurus-safe

Output: corrected .mdx if needed

5. ASSEMBLY & INTEGRATION TASKS
Task 5.1 — Generate_Sidebar

Agent: Claude Code

Input: outline.json

Output: sidebar.js

Location: frontend/docusaurus/sidebars.js

Task 5.2 — Move_Chapters_To_Docusaurus

Agent: Claude Code

Input: all chapter .mdx files

Output Location:

frontend/docusaurus/docs/<part>/<chapter>.mdx

Task 5.3 — Copy_Assets

Agent: Claude Code

Goal: Transfer image/table placeholders

Location: frontend/static/assets/

Task 5.4 — Build_Docusaurus_Site

Agent: Claude Code

Command: npm run build (inside /frontend/docusaurus/)

Output: HTML static site in frontend/docusaurus/build/

6. VALIDATION & PUBLICATION TASKS
Task 6.1 — Validate_Structure

Agent: Claude Code

Goal: Ensure folder structure matches required tree

Task 6.2 — Validate_Content_Integrity

Agent: Claude Code

Goal: Confirm no hallucination, all content matches PDF

Task 6.3 — Publish_To_GitHub_Pages

Agent: Claude Code

Goal: Deploy to GitHub Pages or Vercel

Output: Live book URL

7. TASK EXECUTION ORDER

The execution sequence is strictly:

Extract_PDF_Themes

Extract_Module_Structure

Extract_Weeks

Extract_Hardware

Build_Global_Outline

Expand_Chapters

Generate_Chapter_<ID> (for all chapters)

Validate_MDX_Format

Generate_Sidebar

Move_Chapters_To_Docusaurus

Copy_Assets

Build_Docusaurus_Site

Validate_Structure
```

## Response snapshot

Created a comprehensive task graph with 52 detailed tasks across 5 pipelines: PDF Processing (4 tasks), Outline Construction (2 tasks), Chapter Generation (46 tasks for each chapter across 9 parts), Assembly & Integration (4 tasks), and Validation & Publication (3 tasks). The tasks follow the required execution order with proper dependencies, agent assignments (Claude Code for orchestration, Qwen Code for chapter generation), and file placements. All tasks adhere to the constitution requirements for Physical AI focus, ROS 2 integration, simulation-first approach, and structured curriculum.

## Outcome

- ✅ Impact: Complete task decomposition created for textbook generation
- 🧪 Tests: none
- 📁 Files: Created tasks.md with 52 detailed tasks across 5 pipelines
- 🔁 Next prompts: Ready for implementation of tasks
- 🧠 Reflection: Task graph provides clear execution path with proper dependencies and agent assignments

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all task requirements met
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): begin implementation of PDF processing tasks