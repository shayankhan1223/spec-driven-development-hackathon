# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Physical AI & Embodied Intelligence Focus
All content must relate strictly to Physical AI and Embodied Intelligence concepts, frameworks, and applications. Every chapter, example, and exercise must demonstrate how AI systems interact with the physical world through robotic platforms, sensors, and actuators.

### II. ROS 2 & NVIDIA Isaac Integration
All technical content must be grounded in industry-standard frameworks: Robot Operating System 2 (ROS 2) for robotics middleware and NVIDIA Isaac for AI-accelerated robotics. All code examples, simulations, and hardware integration guides must follow these established platforms.

### III. Simulation-First Development (NON-NEGOTIABLE)
All robotics development follows simulation-first methodology: Gazebo/Unity simulations → validation → hardware deployment. Every concept must include simulation examples before hardware implementation, ensuring safety and reproducibility.

### IV. Vision-Language-Action (VLA) Integration
All AI systems covered must demonstrate Vision-Language-Action pipeline integration. Content must address how perception, reasoning, and action systems work together in embodied AI applications.

### V. Hardware Requirements & Lab Architecture Standards
All content must specify minimum hardware requirements and lab infrastructure. Every chapter must include practical implementation guidance for academic and research laboratory settings with specific hardware recommendations.

### VI. Curriculum Structure & Weekly Breakdown
All content must follow a structured weekly curriculum format with clear learning objectives, practical exercises, assessments, and capstone project integration. Each chapter must map to specific time allocations and learning outcomes.

## Technical Constraints

The project must conform to the required structure:

```
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
```

Content must focus on Physical AI, Embodied Intelligence, ROS 2, Gazebo/Unity Simulation, NVIDIA Isaac/Isaac Sim/Isaac ROS, VLA systems, and humanoid robotics. No additional robotics frameworks or unrelated theories may be introduced without explicit justification from the source PDF.

## Development Workflow

All content generation must follow the Spec-Kit-Plus workflow with Claude Code and Qwen Code agents. Every chapter must undergo deterministic generation, explicit token-efficiency optimization, and production-ready validation. Content must maintain high information-density and authoritative documentation tone.

## Governance

This constitution supersedes all other practices for the Physical AI & Humanoid Robotics textbook project. All agents (Claude Code, Qwen Code, Spec-Kit-Plus components) must follow these principles. Amendments require explicit documentation and approval through the `/sp.constitution` command.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
