# Task Graph: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook
**Date**: 2025-12-07
**Plan**: [plan.md](./plan.md)
**Input**: Physical AI & Humanoid Robotics PDF

## Overview

Complete task decomposition for generating the Physical AI & Humanoid Robotics textbook using Claude Code (orchestrator) and Qwen Code (chapter generator). Tasks follow the required execution order with dependencies clearly defined.

## Pipeline 1: PDF Processing Tasks

### Task 1.1 — Extract_PDF_Themes
- **Agent**: Claude Code
- **Input**: Physical AI & Humanoid Robotics PDF
- **Output**: `backend/processing/themes.json`
- **Goal**: Identify global themes:
  - Physical AI
  - Embodied intelligence
  - ROS 2
  - Gazebo / Unity
  - NVIDIA Isaac
  - VLA
  - Hardware requirements
  - Weekly structure
- **Dependencies**: None
- **Prerequisites**: PDF file exists at specified path
- **Success Criteria**: themes.json contains all 8 theme categories with content references

### Task 1.2 — Extract_Module_Structure
- **Agent**: Claude Code
- **Input**: Physical AI & Humanoid Robotics PDF
- **Output**: `backend/processing/modules.json`
- **Goal**: Map PDF's Modules 1–4 into structured JSON
- **Dependencies**: None
- **Prerequisites**: PDF file exists at specified path
- **Success Criteria**: modules.json contains 4 modules with detailed content breakdown

### Task 1.3 — Extract_Weeks
- **Agent**: Claude Code
- **Input**: Physical AI & Humanoid Robotics PDF
- **Output**: `backend/processing/weeks.json`
- **Goal**: Transform Weeks 1–13 into structured lists
- **Dependencies**: None
- **Prerequisites**: PDF file exists at specified path
- **Success Criteria**: weeks.json contains all 13 weeks with chapter assignments and learning objectives

### Task 1.4 — Extract_Hardware
- **Agent**: Claude Code
- **Input**: Physical AI & Humanoid Robotics PDF
- **Output**: `backend/processing/hardware.json`
- **Goal**: Capture workstation, edge kits, robot lab options, cloud lab, latency constraints
- **Dependencies**: None
- **Prerequisites**: PDF file exists at specified path
- **Success Criteria**: hardware.json contains all hardware specifications with budget tiers and requirements

## Pipeline 2: Outline Construction Tasks

### Task 2.1 — Build_Global_Outline
- **Agent**: Claude Code
- **Input**: `backend/processing/themes.json`, `backend/processing/modules.json`, `backend/processing/weeks.json`
- **Output**: `backend/pipelines/outline.json`
- **Goal**: Convert the book outline defined in sp.plan into structured JSON with 9 parts and 40+ chapters
- **Dependencies**: Tasks 1.1, 1.2, 1.3 completed successfully
- **Success Criteria**: outline.json contains complete 9-part structure with all chapters mapped to weeks

### Task 2.2 — Expand_Chapters
- **Agent**: Claude Code
- **Input**: `backend/pipelines/outline.json`
- **Output**: `backend/pipelines/chapters.json`
- **Goal**: For each chapter, create a generation-ready object with:
  - title
  - key concepts
  - required sections
  - pointers to PDF data
  - expected tables/diagrams
- **Dependencies**: Task 2.1 completed successfully
- **Success Criteria**: chapters.json contains 40+ chapter objects with complete specification data

## Pipeline 3: Chapter Generation Tasks (Qwen Code)

### Task 3.0 — Validate_MDX_Format
- **Agent**: Claude Code
- **Input**: Generated chapter .mdx files
- **Output**: Validated/corrected .mdx files
- **Goal**: Ensure MDX is Docusaurus-safe with proper syntax
- **Dependencies**: All chapter generation tasks completed
- **Success Criteria**: All MDX files pass Docusaurus validation

### Task 3.1 — Generate_Chapter_Introduction_to_Physical_AI
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_i_foundations/introduction_to_physical_ai.mdx`
- **Goal**: Generate chapter following universal template with Overview, Key Concepts, Technical Sections, Examples/Diagrams/Tables, Implementation Notes, Exercises, Summary
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers Physical AI introduction content

### Task 3.2 — Generate_Chapter_Embodied_Intelligence_Physical_Laws
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_i_foundations/embodied_intelligence_physical_laws.mdx`
- **Goal**: Generate chapter following universal template covering embodied intelligence and physical laws
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers embodied intelligence content

### Task 3.3 — Generate_Chapter_Why_Physical_AI_Matters
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_i_foundations/why_physical_ai_matters.mdx`
- **Goal**: Generate chapter following universal template covering importance of Physical AI
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers importance of Physical AI

### Task 3.4 — Generate_Chapter_Emerging_Humanoid_Robotics_Landscape
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_i_foundations/emerging_humanoid_robotics_landscape.mdx`
- **Goal**: Generate chapter following universal template covering humanoid robotics landscape
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers humanoid robotics landscape

### Task 3.5 — Generate_Chapter_ROS2_Architecture_Overview
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ii_ros2/ros2_architecture_overview.mdx`
- **Goal**: Generate chapter following universal template covering ROS 2 architecture
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers ROS 2 architecture

### Task 3.6 — Generate_Chapter_Nodes_Topics_Services_Actions
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ii_ros2/nodes_topics_services_actions.mdx`
- **Goal**: Generate chapter following universal template covering ROS 2 communication primitives
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers ROS 2 communication

### Task 3.7 — Generate_Chapter_ROS2_Packages_Workflows
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ii_ros2/ros2_packages_workflows.mdx`
- **Goal**: Generate chapter following universal template covering ROS 2 packages and workflows
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers ROS 2 packages

### Task 3.8 — Generate_Chapter_URDF_for_Humanoid_Robots
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ii_ros2/urdf_for_humanoid_robots.mdx`
- **Goal**: Generate chapter following universal template covering URDF for humanoid robots
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers URDF content

### Task 3.9 — Generate_Chapter_Launch_Files_Parameter_Management
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ii_ros2/launch_files_parameter_management.mdx`
- **Goal**: Generate chapter following universal template covering launch files and parameters
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers launch files

### Task 3.10 — Generate_Chapter_Simulation_Theory_Gravity_Forces_Collisions
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iii_simulation/simulation_theory_gravity_forces_collisions.mdx`
- **Goal**: Generate chapter following universal template covering simulation theory
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers simulation theory

### Task 3.11 — Generate_Chapter_Gazebo_Physics_Simulation
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iii_simulation/gazebo_physics_simulation.mdx`
- **Goal**: Generate chapter following universal template covering Gazebo physics simulation
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers Gazebo content

### Task 3.12 — Generate_Chapter_Robot_Description_Formats
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iii_simulation/robot_description_formats.mdx`
- **Goal**: Generate chapter following universal template covering robot description formats (URDF → SDF)
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers robot description formats

### Task 3.13 — Generate_Chapter_Unity_for_Humanoid_Visualization
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iii_simulation/unity_for_humanoid_visualization.mdx`
- **Goal**: Generate chapter following universal template covering Unity for humanoid visualization
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers Unity content

### Task 3.14 — Generate_Chapter_Sensor_Simulation_LiDAR_Depth_IMU
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iii_simulation/sensor_simulation_lidar_depth_imu.mdx`
- **Goal**: Generate chapter following universal template covering sensor simulation
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers sensor simulation

### Task 3.15 — Generate_Chapter_Isaac_Sim_Fundamentals
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iv_isaac/isaac_sim_fundamentals.mdx`
- **Goal**: Generate chapter following universal template covering Isaac Sim fundamentals
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers Isaac Sim fundamentals

### Task 3.16 — Generate_Chapter_Synthetic_Data_Photorealistic_Rendering
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iv_isaac/synthetic_data_photorealistic_rendering.mdx`
- **Goal**: Generate chapter following universal template covering synthetic data and rendering
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers synthetic data content

### Task 3.17 — Generate_Chapter_Isaac_ROS_VSLAM_Perception
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iv_isaac/isaac_ros_vslam_perception.mdx`
- **Goal**: Generate chapter following universal template covering Isaac ROS perception
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers Isaac ROS content

### Task 3.18 — Generate_Chapter_Nav2_Path_Planning_Bipedal_Robots
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iv_isaac/nav2_path_planning_bipedal_robots.mdx`
- **Goal**: Generate chapter following universal template covering Nav2 for bipedal robots
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers Nav2 content

### Task 3.19 — Generate_Chapter_Reinforcement_Learning_Control
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iv_isaac/reinforcement_learning_control.mdx`
- **Goal**: Generate chapter following universal template covering reinforcement learning for control
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers reinforcement learning

### Task 3.20 — Generate_Chapter_Sim_to_Real_Transfer
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_iv_isaac/sim_to_real_transfer.mdx`
- **Goal**: Generate chapter following universal template covering sim-to-real transfer
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers sim-to-real content

### Task 3.21 — Generate_Chapter_Humanoid_Kinematics
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_v_humanoid/humanoid_kinematics.mdx`
- **Goal**: Generate chapter following universal template covering humanoid kinematics
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers kinematics content

### Task 3.22 — Generate_Chapter_Humanoid_Dynamics
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_v_humanoid/humanoid_dynamics.mdx`
- **Goal**: Generate chapter following universal template covering humanoid dynamics
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers dynamics content

### Task 3.23 — Generate_Chapter_Bipedal_Locomotion_Balance
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_v_humanoid/bipedal_locomotion_balance.mdx`
- **Goal**: Generate chapter following universal template covering bipedal locomotion and balance
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers locomotion content

### Task 3.24 — Generate_Chapter_Manipulation_Grasping
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_v_humanoid/manipulation_grasping.mdx`
- **Goal**: Generate chapter following universal template covering manipulation and grasping
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers manipulation content

### Task 3.25 — Generate_Chapter_Human_Robot_Interaction_Design
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_v_humanoid/human_robot_interaction_design.mdx`
- **Goal**: Generate chapter following universal template covering human-robot interaction design
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers interaction design

### Task 3.26 — Generate_Chapter_Voice_to_Action_Whisper_Integration
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vi_vla/voice_to_action_whisper_integration.mdx`
- **Goal**: Generate chapter following universal template covering voice-to-action with Whisper
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers voice integration

### Task 3.27 — Generate_Chapter_Natural_Language_ROS2_Plans
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vi_vla/natural_language_ros2_plans.mdx`
- **Goal**: Generate chapter following universal template covering natural language to ROS 2 plans
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers NLP content

### Task 3.28 — Generate_Chapter_LLM_Cognitive_Planning
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vi_vla/llm_cognitive_planning.mdx`
- **Goal**: Generate chapter following universal template covering LLM cognitive planning
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers cognitive planning

### Task 3.29 — Generate_Chapter_Multimodal_Interaction
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vi_vla/multimodal_interaction.mdx`
- **Goal**: Generate chapter following universal template covering multimodal interaction (speech, gesture, vision)
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers multimodal content

### Task 3.30 — Generate_Chapter_Digital_Twin_Workstation_Requirements
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vii_hardware/digital_twin_workstation_requirements.mdx`
- **Goal**: Generate chapter following universal template covering digital twin workstation requirements
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers workstation requirements

### Task 3.31 — Generate_Chapter_Physical_AI_Edge_Kits_Jetson
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vii_hardware/physical_ai_edge_kits_jetson.mdx`
- **Goal**: Generate chapter following universal template covering Physical AI edge kits (Jetson)
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers Jetson kits

### Task 3.32 — Generate_Chapter_Robot_Lab_Options
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vii_hardware/robot_lab_options.mdx`
- **Goal**: Generate chapter following universal template covering robot lab options (proxy/minature/premium)
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers lab options

### Task 3.33 — Generate_Chapter_Physical_AI_Architecture_Summary
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vii_hardware/physical_ai_architecture_summary.mdx`
- **Goal**: Generate chapter following universal template covering Physical AI architecture summary
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers architecture content

### Task 3.34 — Generate_Chapter_Cloud_Native_Ether_Lab
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vii_hardware/cloud_native_ether_lab.mdx`
- **Goal**: Generate chapter following universal template covering cloud-native "ether lab"
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers cloud lab content

### Task 3.35 — Generate_Chapter_Economy_Jetson_Student_Kit
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vii_hardware/economy_jetson_student_kit.mdx`
- **Goal**: Generate chapter following universal template covering economy Jetson student kit
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers student kit content

### Task 3.36 — Generate_Chapter_Latency_Trap_Safety_Requirements
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_vii_hardware/latency_trap_safety_requirements.mdx`
- **Goal**: Generate chapter following universal template covering latency trap and safety requirements
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers safety content

### Task 3.37 — Generate_Chapter_Week_1_2_Physical_AI_Foundations
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_viii_weekly/week_1_2_physical_ai_foundations.mdx`
- **Goal**: Generate chapter following universal template covering Weeks 1-2 curriculum
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers weeks 1-2 content

### Task 3.38 — Generate_Chapter_Week_3_5_ROS2_Fundamentals
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_viii_weekly/week_3_5_ros2_fundamentals.mdx`
- **Goal**: Generate chapter following universal template covering Weeks 3-5 curriculum
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers weeks 3-5 content

### Task 3.39 — Generate_Chapter_Week_6_7_Gazebo_Simulation
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_viii_weekly/week_6_7_gazebo_simulation.mdx`
- **Goal**: Generate chapter following universal template covering Weeks 6-7 curriculum
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers weeks 6-7 content

### Task 3.40 — Generate_Chapter_Week_8_10_NVIDIA_Isaac
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_viii_weekly/week_8_10_nvidia_isaac.mdx`
- **Goal**: Generate chapter following universal template covering Weeks 8-10 curriculum
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers weeks 8-10 content

### Task 3.41 — Generate_Chapter_Week_11_12_Humanoid_Robotics
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_viii_weekly/week_11_12_humanoid_robotics.mdx`
- **Goal**: Generate chapter following universal template covering Weeks 11-12 curriculum
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers weeks 11-12 content

### Task 3.42 — Generate_Chapter_Week_13_Conversational_Robotics
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_viii_weekly/week_13_conversational_robotics.mdx`
- **Goal**: Generate chapter following universal template covering Week 13 curriculum
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers week 13 content

### Task 3.43 — Generate_Chapter_ROS2_Package_Project
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ix_assessments/ros2_package_project.mdx`
- **Goal**: Generate chapter following universal template covering ROS 2 package project assessment
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers assessment content

### Task 3.44 — Generate_Chapter_Gazebo_Simulation_Project
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ix_assessments/gazebo_simulation_project.mdx`
- **Goal**: Generate chapter following universal template covering Gazebo simulation project assessment
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers assessment content

### Task 3.45 — Generate_Chapter_Isaac_Perception_Pipeline
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ix_assessments/isaac_perception_pipeline.mdx`
- **Goal**: Generate chapter following universal template covering Isaac perception pipeline assessment
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers assessment content

### Task 3.46 — Generate_Chapter_Capstone_Autonomous_Humanoid_Robot
- **Agent**: Qwen Code
- **Input**: Chapter spec from `backend/pipelines/chapters.json`
- **Output**: `book_output/part_ix_assessments/capstone_autonomous_humanoid_robot.mdx`
- **Goal**: Generate chapter following universal template covering capstone autonomous humanoid robot project
- **Dependencies**: Task 2.2 completed successfully
- **Success Criteria**: Chapter file follows template and covers capstone content

## Pipeline 4: Assembly & Integration Tasks

### Task 4.1 — Generate_Sidebar
- **Agent**: Claude Code
- **Input**: `backend/pipelines/outline.json`
- **Output**: `frontend/docusaurus/sidebars.js`
- **Goal**: Create Docusaurus sidebar configuration that matches the book outline structure
- **Dependencies**: Task 2.1 completed successfully
- **Success Criteria**: sidebar.js properly organizes all 9 parts and 40+ chapters with correct hierarchy

### Task 4.2 — Move_Chapters_To_Docusaurus
- **Agent**: Claude Code
- **Input**: All chapter .mdx files from `book_output/`
- **Output**: Files moved to `frontend/docusaurus/docs/<part>/`
- **Goal**: Transfer all generated chapters to Docusaurus docs directory with proper folder structure
- **Dependencies**: All chapter generation tasks (3.1-3.46) and Task 3.0 completed successfully
- **Success Criteria**: All 40+ chapters exist in the correct Docusaurus docs structure

### Task 4.3 — Copy_Assets
- **Agent**: Claude Code
- **Input**: Image/table placeholders from processing
- **Output**: Assets copied to `frontend/static/assets/`
- **Goal**: Transfer image, diagram, and table assets for textbook content
- **Dependencies**: All chapter generation tasks completed
- **Success Criteria**: All referenced assets exist in the static assets directory

### Task 4.4 — Build_Docusaurus_Site
- **Agent**: Claude Code
- **Input**: Complete Docusaurus project with docs and assets
- **Output**: Static site in `frontend/docusaurus/build/`
- **Goal**: Execute `npm run build` to generate the final textbook website
- **Dependencies**: Tasks 4.1, 4.2, 4.3 completed successfully
- **Success Criteria**: Build completes successfully with no errors, generates complete static site

## Pipeline 5: Validation & Publication Tasks

### Task 5.1 — Validate_Structure
- **Agent**: Claude Code
- **Input**: Generated textbook files and folder structure
- **Output**: Validation report
- **Goal**: Ensure folder structure matches required tree from constitution
- **Dependencies**: Task 4.4 completed successfully
- **Success Criteria**: All files exist in correct locations according to required structure

### Task 5.2 — Validate_Content_Integrity
- **Agent**: Claude Code
- **Input**: Generated textbook content
- **Output**: Integrity validation report
- **Goal**: Confirm no hallucination, all content matches PDF source material
- **Dependencies**: Task 4.4 completed successfully
- **Success Criteria**: Content accuracy verified against source PDF, no hallucinated information

### Task 5.3 — Publish_To_GitHub_Pages
- **Agent**: Claude Code
- **Input**: Built static site from `frontend/docusaurus/build/`
- **Output**: Live book URL
- **Goal**: Deploy to GitHub Pages or Vercel hosting platform
- **Dependencies**: Tasks 5.1, 5.2 completed successfully
- **Success Criteria**: Textbook is live and accessible at published URL

## Execution Order

The tasks must execute in the following strict sequence:

1. PDF Processing Tasks (1.1 - 1.4) - Can run in parallel
2. Outline Construction Tasks (2.1 - 2.2) - Sequential
3. Chapter Generation Tasks (3.1 - 3.46) - Can run in parallel after 2.2
4. MDX Validation Task (3.0) - After all chapter generation
5. Assembly Tasks (4.1 - 4.4) - Sequential
6. Validation Tasks (5.1 - 5.2) - Can run in parallel
7. Publication Task (5.3) - After all validations

## Success Criteria

- All 46 chapter files generated in correct locations
- Docusaurus site builds without errors
- Content matches PDF source material
- Textbook is successfully published and accessible
- All constitution requirements satisfied (Physical AI focus, ROS 2 integration, etc.)