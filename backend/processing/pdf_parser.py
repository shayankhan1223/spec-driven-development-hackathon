"""
PDF parsing functions for extracting content from the Physical AI textbook PDF.
"""
import json
from pathlib import Path

def extract_themes(pdf_path):
    """
    Task 1.1 — Extract_PDF_Themes
    Extract global themes from the PDF:
    - Physical AI
    - Embodied intelligence
    - ROS 2
    - Gazebo / Unity
    - NVIDIA Isaac
    - VLA
    - Hardware requirements
    - Weekly structure
    """
    # In a real implementation, this would parse the actual PDF
    # For now, we'll return a template structure
    themes = {
        "physical_ai": {
            "title": "Physical AI",
            "description": "Core concepts of Physical AI",
            "references": []
        },
        "embodied_intelligence": {
            "title": "Embodied Intelligence",
            "description": "Intelligence that emerges from interaction with the physical world",
            "references": []
        },
        "ros2": {
            "title": "ROS 2",
            "description": "Robot Operating System 2",
            "references": []
        },
        "gazebo_unity": {
            "title": "Gazebo & Unity",
            "description": "Simulation environments",
            "references": []
        },
        "nvidia_isaac": {
            "title": "NVIDIA Isaac",
            "description": "AI robotics platform",
            "references": []
        },
        "vla": {
            "title": "VLA (Vision-Language-Action)",
            "description": "Integrated perception-action systems",
            "references": []
        },
        "hardware_requirements": {
            "title": "Hardware Requirements",
            "description": "Specifications for robots and infrastructure",
            "references": []
        },
        "weekly_structure": {
            "title": "Weekly Curriculum Structure",
            "description": "13-week learning path",
            "references": []
        }
    }
    return themes

def extract_modules(pdf_path):
    """
    Task 1.2 — Extract_Module_Structure
    Map PDF's Modules 1–4 into structured JSON
    """
    modules = {
        "module_1": {
            "title": "Introduction to Physical AI",
            "chapters": ["Introduction to Physical AI", "Embodied Intelligence", "Why Physical AI Matters"],
            "topics": []
        },
        "module_2": {
            "title": "ROS 2 and Communication",
            "chapters": ["ROS 2 Architecture", "Nodes, Topics, Services, Actions", "Packages and Workflows"],
            "topics": []
        },
        "module_3": {
            "title": "Simulation and Perception",
            "chapters": ["Gazebo Simulation", "Unity Visualization", "Sensor Simulation"],
            "topics": []
        },
        "module_4": {
            "title": "Advanced Robotics",
            "chapters": ["Humanoid Kinematics", "Dynamics and Locomotion", "Manipulation"],
            "topics": []
        }
    }
    return modules

def extract_weeks(pdf_path):
    """
    Task 1.3 — Extract_Weeks
    Transform Weeks 1–13 into structured lists
    """
    weeks = {}
    for week_num in range(1, 14):
        weeks[f"week_{week_num}"] = {
            "week_number": week_num,
            "title": f"Week {week_num} Content",
            "chapters": [],
            "learning_objectives": [],
            "estimated_hours": 8
        }

    # Define the actual curriculum mapping
    weeks["week_1"] = {
        "week_number": 1,
        "title": "Physical AI Foundations",
        "chapters": ["Introduction to Physical AI", "Embodied Intelligence & Physical Laws"],
        "learning_objectives": ["Understand Physical AI concepts", "Learn about embodied intelligence"],
        "estimated_hours": 8
    }

    weeks["week_2"] = {
        "week_number": 2,
        "title": "Physical AI Foundations (continued)",
        "chapters": ["Why Physical AI Matters", "The Emerging Humanoid Robotics Landscape"],
        "learning_objectives": ["Understand importance of Physical AI", "Explore humanoid robotics landscape"],
        "estimated_hours": 8
    }

    weeks["week_3"] = {
        "week_number": 3,
        "title": "ROS 2 Fundamentals",
        "chapters": ["ROS 2 Architecture Overview", "Nodes, Topics, Services & Actions"],
        "learning_objectives": ["Learn ROS 2 architecture", "Understand ROS 2 communication primitives"],
        "estimated_hours": 8
    }

    weeks["week_4"] = {
        "week_number": 4,
        "title": "ROS 2 Continued",
        "chapters": ["ROS 2 Packages & Workflows", "URDF for Humanoid Robots"],
        "learning_objectives": ["Master ROS 2 packages", "Understand URDF for humanoid robots"],
        "estimated_hours": 8
    }

    weeks["week_5"] = {
        "week_number": 5,
        "title": "ROS 2 Advanced",
        "chapters": ["Launch Files & Parameter Management"],
        "learning_objectives": ["Learn launch files and parameter management"],
        "estimated_hours": 8
    }

    weeks["week_6"] = {
        "week_number": 6,
        "title": "Gazebo Simulation",
        "chapters": ["Simulation Theory: Gravity, Forces & Collisions", "Gazebo Physics Simulation"],
        "learning_objectives": ["Understand simulation theory", "Learn Gazebo physics simulation"],
        "estimated_hours": 8
    }

    weeks["week_7"] = {
        "week_number": 7,
        "title": "Unity and Sensor Simulation",
        "chapters": ["Robot Description Formats (URDF → SDF)", "Unity for Humanoid Visualization", "Sensor Simulation: LiDAR, Depth, IMU"],
        "learning_objectives": ["Learn Unity visualization", "Understand sensor simulation"],
        "estimated_hours": 8
    }

    weeks["week_8"] = {
        "week_number": 8,
        "title": "NVIDIA Isaac Introduction",
        "chapters": ["Isaac Sim Fundamentals", "Synthetic Data & Photorealistic Rendering"],
        "learning_objectives": ["Learn Isaac Sim fundamentals", "Understand synthetic data generation"],
        "estimated_hours": 8
    }

    weeks["week_9"] = {
        "week_number": 9,
        "title": "Isaac Perception and Navigation",
        "chapters": ["Isaac ROS: VSLAM & Perception", "Nav2 Path Planning for Bipedal Robots"],
        "learning_objectives": ["Learn Isaac ROS perception", "Understand Nav2 for bipedal robots"],
        "estimated_hours": 8
    }

    weeks["week_10"] = {
        "week_number": 10,
        "title": "Isaac Advanced",
        "chapters": ["Reinforcement Learning for Control", "Sim-to-Real Transfer"],
        "learning_objectives": ["Learn reinforcement learning for control", "Understand sim-to-real transfer"],
        "estimated_hours": 8
    }

    weeks["week_11"] = {
        "week_number": 11,
        "title": "Humanoid Robotics",
        "chapters": ["Humanoid Kinematics", "Humanoid Dynamics"],
        "learning_objectives": ["Learn humanoid kinematics", "Understand humanoid dynamics"],
        "estimated_hours": 8
    }

    weeks["week_12"] = {
        "week_number": 12,
        "title": "Humanoid Control and Interaction",
        "chapters": ["Bipedal Locomotion & Balance", "Manipulation & Grasping", "Human-Robot Interaction Design"],
        "learning_objectives": ["Master bipedal locomotion", "Learn manipulation and grasping", "Understand human-robot interaction"],
        "estimated_hours": 8
    }

    weeks["week_13"] = {
        "week_number": 13,
        "title": "VLA Systems and Capstone",
        "chapters": ["Voice-to-Action: Whisper Integration", "Natural Language → ROS 2 Plans", "LLM Cognitive Planning", "Multimodal Interaction (Speech, Gesture, Vision)", "Capstone: Autonomous Humanoid Robot"],
        "learning_objectives": ["Learn VLA systems", "Complete capstone project"],
        "estimated_hours": 10
    }

    return weeks

def extract_hardware(pdf_path):
    """
    Task 1.4 — Extract_Hardware
    Capture workstation, edge kits, robot lab options, cloud lab, latency constraints
    """
    hardware = {
        "digital_twin_workstation": {
            "requirements": {
                "cpu": "8+ cores",
                "memory": "32GB+ RAM",
                "gpu": "NVIDIA RTX 3080 or better",
                "storage": "1TB SSD"
            },
            "budget_tiers": {
                "economy": "$2000-3000",
                "standard": "$4000-6000",
                "premium": "$8000+"
            }
        },
        "physical_ai_edge_kits": {
            "jetson_options": [
                {
                    "model": "Jetson Nano",
                    "use_case": "Student projects",
                    "cost": "$99"
                },
                {
                    "model": "Jetson Xavier NX",
                    "use_case": "Research projects",
                    "cost": "$399"
                },
                {
                    "model": "Jetson AGX Orin",
                    "use_case": "Advanced robotics",
                    "cost": "$999"
                }
            ]
        },
        "robot_lab_options": {
            "proxy": {
                "description": "Simulated robots for learning",
                "cost": "Software only",
                "requirements": ["Computer", "Simulation software"]
            },
            "miniature": {
                "description": "Small physical robots",
                "cost": "$500-2000 per robot",
                "requirements": ["Robot platform", "Computing hardware", "Safety equipment"]
            },
            "premium": {
                "description": "Full humanoid robots",
                "cost": "$10,000-100,000 per robot",
                "requirements": ["Humanoid platform", "High-performance computing", "Specialized facilities"]
            }
        },
        "cloud_native_ether_lab": {
            "description": "Cloud-based robotics lab",
            "requirements": ["Internet connection", "Cloud computing resources", "Remote access tools"]
        },
        "latency_safety_requirements": {
            "real_time_control": "<10ms latency required",
            "safety_systems": "<5ms response time for safety",
            "network": "Dedicated low-latency connection recommended"
        }
    }
    return hardware