# Data Model: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook
**Date**: 2025-12-07
**Status**: Complete

## Overview

This document defines the key data entities and structures for the Physical AI & Humanoid Robotics textbook generation system. These entities represent the core concepts that will be processed, stored, and generated throughout the textbook creation pipeline.

## Core Entities

### 1. TextbookChapter

**Description**: Represents a single chapter in the Physical AI textbook

**Fields**:
- `id`: Unique identifier for the chapter
- `title`: Chapter title from the source PDF
- `part`: Part number (I-IX) that the chapter belongs to
- `week`: Week number (1-13) if applicable
- `content`: Raw content extracted from PDF
- `structuredContent`: Processed content following chapter template
- `learningObjectives`: List of learning objectives for the chapter
- `technicalConcepts`: List of key technical concepts covered
- `examples`: List of code examples or diagrams
- `exercises`: List of exercises at the end of the chapter
- `prerequisites`: List of prerequisite knowledge required
- `relatedChapters`: List of related chapters for cross-referencing
- `createdAt`: Timestamp of creation
- `updatedAt`: Timestamp of last update

**Validation Rules**:
- Title must not be empty
- Part must be between I and IX
- Week must be between 1 and 13 (if applicable)
- Content must follow the chapter template structure

### 2. TextbookPart

**Description**: Represents one of the 9 major parts of the textbook

**Fields**:
- `id`: Unique identifier for the part
- `partNumber`: Roman numeral identifier (I-IX)
- `title`: Full title of the part
- `description`: Brief description of the part's content
- `chapters`: List of chapters belonging to this part
- `learningPath`: Sequential order of chapters within the part
- `createdAt`: Timestamp of creation
- `updatedAt`: Timestamp of last update

**Validation Rules**:
- Part number must be between I and IX
- Title must match one of the predefined part titles
- Must contain at least one chapter

### 3. CurriculumWeek

**Description**: Represents a week in the 13-week learning curriculum

**Fields**:
- `id`: Unique identifier for the week
- `weekNumber`: Week number (1-13)
- `title`: Title of the week's focus
- `chapters`: List of chapters to be covered in the week
- `learningObjectives`: Overall objectives for the week
- `estimatedHours`: Estimated hours of study for the week
- `prerequisites`: Prerequisites needed before this week
- `assessment`: Type of assessment for the week
- `createdAt`: Timestamp of creation
- `updatedAt`: Timestamp of last update

**Validation Rules**:
- Week number must be between 1 and 13
- Estimated hours must be positive
- Must have at least one chapter assigned

### 4. TechnicalConcept

**Description**: Represents a specific technical concept from the textbook (ROS 2, NVIDIA Isaac, etc.)

**Fields**:
- `id`: Unique identifier for the concept
- `name`: Name of the technical concept
- `category`: Category (ROS 2, NVIDIA Isaac, Simulation, etc.)
- `definition`: Definition of the concept
- `examples`: List of examples demonstrating the concept
- `relatedConcepts`: List of related technical concepts
- `difficulty`: Difficulty level (Beginner, Intermediate, Advanced)
- `createdAt`: Timestamp of creation
- `updatedAt`: Timestamp of last update

**Validation Rules**:
- Name must not be empty
- Category must be one of the predefined categories
- Difficulty must be one of: Beginner, Intermediate, Advanced

### 5. HardwareSpecification

**Description**: Represents hardware requirements and specifications mentioned in the textbook

**Fields**:
- `id`: Unique identifier for the hardware spec
- `name`: Name of the hardware component or system
- `type`: Type of hardware (Workstation, Robot, Sensor, etc.)
- `requirements`: Detailed requirements for the hardware
- `budgetTier`: Budget level (Economy, Standard, Premium)
- `useCase`: Primary use case for this hardware
- `alternatives`: List of alternative options
- `costEstimate`: Estimated cost for the hardware
- `createdAt`: Timestamp of creation
- `updatedAt`: Timestamp of last update

**Validation Rules**:
- Name must not be empty
- Budget tier must be one of: Economy, Standard, Premium
- Cost estimate must be non-negative

### 6. ContentProcessingTask

**Description**: Represents a task in the content processing pipeline

**Fields**:
- `id`: Unique identifier for the task
- `taskId`: External identifier for the task in the pipeline
- `chapterId`: ID of the chapter being processed
- `taskType`: Type of task (extraction, transformation, generation)
- `status`: Current status (pending, processing, completed, failed)
- `inputFile`: Path to the input file for processing
- `outputFile`: Path to the output file after processing
- `error`: Error message if the task failed
- `createdAt`: Timestamp of task creation
- `updatedAt`: Timestamp of last update
- `completedAt`: Timestamp of task completion

**Validation Rules**:
- Task type must be one of: extraction, transformation, generation
- Status must be one of: pending, processing, completed, failed
- Chapter ID must reference an existing chapter

## Relationships

### TextbookPart and TextbookChapter
- One TextbookPart contains many TextbookChapters
- Each TextbookChapter belongs to exactly one TextbookPart

### CurriculumWeek and TextbookChapter
- One CurriculumWeek contains many TextbookChapters
- Each TextbookChapter may belong to zero or one CurriculumWeek

### TextbookChapter and TechnicalConcept
- One TextbookChapter covers many TechnicalConcepts
- One TechnicalConcept may be covered in many TextbookChapters

### TextbookChapter and HardwareSpecification
- One TextbookChapter may reference many HardwareSpecifications
- One HardwareSpecification may be referenced in many TextbookChapters

### ContentProcessingTask and TextbookChapter
- One ContentProcessingTask processes exactly one TextbookChapter
- One TextbookChapter may have many ContentProcessingTasks (for different processing stages)

## State Transitions

### ContentProcessingTask Status Transitions
- `pending` → `processing` (when task starts execution)
- `processing` → `completed` (when task finishes successfully)
- `processing` → `failed` (when task encounters an error)
- `failed` → `pending` (when task is retried)

## Data Validation

### Required Fields
All entities have required fields that must be present:
- ID field for unique identification
- CreatedAt timestamp for tracking creation time
- UpdatedAt timestamp for tracking modification time

### Constraints
- All timestamps must be in ISO 8601 format
- All text fields must be UTF-8 encoded
- All numeric fields must be within reasonable bounds
- All foreign key references must point to existing entities