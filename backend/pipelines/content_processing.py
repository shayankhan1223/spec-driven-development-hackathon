"""
Pipeline for expanding chapters from the global outline.
"""
import json

def expand_chapters(outline_path):
    """
    Task 2.2 — Expand_Chapters
    For each chapter, create a generation-ready object with:
    - title
    - key concepts
    - required sections
    - pointers to PDF data
    - expected tables/diagrams
    """
    with open(outline_path, 'r') as f:
        outline = json.load(f)

    chapters = []

    # Process each part and its chapters
    for part in outline['parts']:
        for chapter in part['chapters']:
            chapter_spec = {
                "id": chapter['id'],
                "title": chapter['title'],
                "part": part['part_number'],
                "part_title": part['title'],
                "description": part['description'],
                "sections": chapter['sections'],
                "week": chapter.get('week', 'N/A'),
                "key_concepts": [],
                "required_tables": [],
                "required_diagrams": [],
                "source_refs": [],
                "learning_objectives": [],
                "prerequisites": [],
                "exercises": [],
                "technical_concepts": [],
                "hardware_specs": []
            }

            # Add specific key concepts based on the chapter topic
            if "physical ai" in chapter['title'].lower():
                chapter_spec["key_concepts"] = [
                    "Physical AI definition",
                    "Embodied intelligence",
                    "Real-world interaction",
                    "Sensorimotor integration"
                ]
                chapter_spec["learning_objectives"] = [
                    "Define Physical AI and its importance",
                    "Distinguish from traditional AI approaches",
                    "Understand embodied intelligence principles"
                ]

            elif "ros2" in chapter['title'].lower():
                chapter_spec["key_concepts"] = [
                    "ROS 2 architecture",
                    "Communication primitives",
                    "Package management",
                    "Launch systems"
                ]
                chapter_spec["technical_concepts"] = [
                    "Nodes",
                    "Topics",
                    "Services",
                    "Actions",
                    "Parameters"
                ]
                chapter_spec["learning_objectives"] = [
                    "Understand ROS 2 architecture",
                    "Implement basic ROS 2 communication",
                    "Create and manage ROS 2 packages"
                ]

            elif "simulation" in chapter['title'].lower():
                chapter_spec["key_concepts"] = [
                    "Physics simulation",
                    "Collision detection",
                    "Force modeling",
                    "Digital twins"
                ]
                chapter_spec["required_diagrams"] = [
                    "Simulation architecture",
                    "Physics engine workflow",
                    "Gazebo/Unity comparison"
                ]
                chapter_spec["learning_objectives"] = [
                    "Set up physics simulation environments",
                    "Model physical interactions",
                    "Validate simulation accuracy"
                ]

            elif "isaac" in chapter['title'].lower():
                chapter_spec["key_concepts"] = [
                    "NVIDIA Isaac platform",
                    "Synthetic data generation",
                    "Perception systems",
                    "Navigation"
                ]
                chapter_spec["technical_concepts"] = [
                    "Isaac Sim",
                    "Isaac ROS",
                    "VSLAM",
                    "Nav2"
                ]
                chapter_spec["learning_objectives"] = [
                    "Deploy Isaac Sim for robotics",
                    "Implement perception pipelines",
                    "Configure navigation systems"
                ]

            elif "humanoid" in chapter['title'].lower() or "kinematics" in chapter['title'].lower() or "dynamics" in chapter['title'].lower():
                chapter_spec["key_concepts"] = [
                    "Humanoid robot design",
                    "Kinematic chains",
                    "Dynamic modeling",
                    "Balance control"
                ]
                chapter_spec["technical_concepts"] = [
                    "Forward kinematics",
                    "Inverse kinematics",
                    "Center of mass control",
                    "Zero moment point"
                ]
                chapter_spec["learning_objectives"] = [
                    "Analyze humanoid kinematics",
                    "Model dynamic behavior",
                    "Implement balance control"
                ]

            elif "vla" in chapter['title'].lower() or "vision-language" in chapter['title'].lower() or "voice" in chapter['title'].lower():
                chapter_spec["key_concepts"] = [
                    "Vision-Language-Action integration",
                    "Multimodal perception",
                    "Language grounding",
                    "Action planning"
                ]
                chapter_spec["technical_concepts"] = [
                    "Large language models",
                    "Computer vision",
                    "Action execution",
                    "Multimodal fusion"
                ]
                chapter_spec["learning_objectives"] = [
                    "Integrate vision and language",
                    "Map language to actions",
                    "Implement multimodal systems"
                ]

            elif "hardware" in chapter['title'].lower() or "lab" in chapter['title'].lower():
                chapter_spec["key_concepts"] = [
                    "Hardware requirements",
                    "System architecture",
                    "Performance constraints",
                    "Safety considerations"
                ]
                chapter_spec["hardware_specs"] = [
                    "Computing requirements",
                    "Sensor specifications",
                    "Network requirements",
                    "Safety systems"
                ]
                chapter_spec["learning_objectives"] = [
                    "Specify hardware requirements",
                    "Design system architecture",
                    "Evaluate performance trade-offs"
                ]

            elif "assessment" in chapter['title'].lower() or "project" in chapter['title'].lower() or "capstone" in chapter['title'].lower():
                chapter_spec["key_concepts"] = [
                    "Project planning",
                    "System integration",
                    "Evaluation metrics",
                    "Documentation"
                ]
                chapter_spec["learning_objectives"] = [
                    "Plan complex robotics projects",
                    "Integrate multiple systems",
                    "Evaluate project outcomes",
                    "Document technical work"
                ]

            # Add common elements to all chapters
            chapter_spec["required_tables"] = [
                "Key terms and definitions",
                "Technical specifications",
                "Comparison matrices"
            ]

            chapter_spec["exercises"] = [
                "Conceptual questions",
                "Practical implementation tasks",
                "Analysis problems"
            ]

            chapter_spec["prerequisites"] = [
                "Basic programming skills",
                "Mathematics fundamentals",
                "Introduction to robotics concepts"
            ]

            chapters.append(chapter_spec)

    return chapters