---
id: 1
title: Update Physical AI Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: /sp.constitution
labels: [constitution, physical-ai, humanoid-robotics, textbook]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
SYSTEM PURPOSE:
Define the global reasoning rules, formatting constraints, output discipline, and behavioral principles that every subsequent prompt in this book-building workflow must follow. These rules bind all agents (Claude Code, Qwen Code, Spec-Kit-Plus components).

1. GLOBAL REASONING PRINCIPLES

Always reason in a strictly deterministic, step-by-step manner.

Never infer or hallucinate topics not explicitly grounded in the provided PDF.

Prefer precision, hierarchy, and explicit structure over verbosity.

Every output must remain consistent with:

the extracted themes from the source PDF

the Docusaurus book structure

the engineering workflow (Claude Code + Qwen Code API)

Maintain unambiguous separation between:

planning

specification

generation

assembly

Always optimize for long-term maintainability, reproducibility, and stable regeneration.

2. CONTENT & DOMAIN RULES

All content must relate strictly to the themes from the Physical AI & Humanoid Robotics textbook source PDF:

Physical AI

Embodied Intelligence

ROS 2

Gazebo / Unity Simulation

NVIDIA Isaac / Isaac Sim / Isaac ROS

VLA (Vision-Language-Action)

Humanoid robotics

Hardware requirements & lab architectures

Weekly curriculum breakdown

Assessments and capstone

Do not introduce additional robotics frameworks, hardware, or unrelated robotics theory.

Never include fictional examples, hypothetical research, or speculative future technologies unless explicitly derived from the PDF.

3. FORMATTING RULES

All outputs must follow the formatting style defined below:

3.1. Structural Formatting

Always use:

clear section dividers

hierarchical headings (H1 → H4)

numbered lists

deterministic bullet structures

Every prompt or spec must begin with an H1 title.

All instructions must be numbered; sub-steps must be alphabetized.

3.2. Code & File Structure Requirements

All referenced code, pipelines, or commands must conform to the required structure:

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


No deviations are allowed.

4. OUTPUT QUALITY RULES

Every output must be:

concise

technically precise

production-ready

free of filler language

All text must maintain:

high information-density

unified technical voice

authoritative documentation tone

When generating content for Qwen Code:

ensure explicit token-efficiency

avoid redundant regeneration steps

provide deterministic chapter structures

When generating instructions for Claude Code:

orchestrator logic must be explicit

pipelines must be modular

responsibilities must not overlap between agents

5. INTERACTION RULES

You (the system) must always output only one prompt at a time.

Wait for the user to say "Next" before producing the next prompt in the workflow.

The workflow order is immutable:

sp.constitution

specify

p
```

## Response snapshot

Updated the constitution file to reflect the Physical AI & Humanoid Robotics textbook project requirements, replacing all placeholder tokens with specific content focused on Physical AI, Embodied Intelligence, ROS 2, NVIDIA Isaac, simulation-first development, Vision-Language-Action integration, hardware requirements, and curriculum structure.

## Outcome

- ✅ Impact: Updated constitution to align with Physical AI & Humanoid Robotics project requirements
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Next step in workflow would be /sp.specify
- 🧠 Reflection: Constitution now properly reflects the specific requirements for the Physical AI textbook project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - constitution properly updated
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): proceed with /sp.specify to continue workflow