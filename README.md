# Smart Task Manager with Priority Scheduling

A sophisticated productivity tool built with Python and Tkinter that automatically reorders tasks based on urgency, dependencies, and deadlines.

## Features

### Core Functionality
- **Smart Priority Scheduling**: Automatic task reordering based on calculated priority scores
- **Task Dependency Management**: Handles task dependencies with topological sorting
- **Deadline Urgency Calculation**: Dynamic priority calculation based on approaching deadlines
- **Real-time Updates**: Priority scores update automatically as deadlines approach

### User Interface
- **Modern GUI**: Clean, intuitive Tkinter-based interface
- **Color-coded Tasks**: Visual indicators for overdue, due soon, and high-priority tasks
- **Interactive Task List**: Sortable table with detailed task information
- **Task Details**: Double-click tasks to view comprehensive details
- **Real-time Clock**: Current time display in the header

### Data Management
- **JSON Persistence**: Save and load task data in JSON format
- **CSV Export**: Export tasks to CSV for external analysis
- **Data Validation**: Input validation and error handling
- **Sample Data**: Pre-loaded demonstration tasks

## Installation and Setup

### Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python)
- No additional dependencies required

### Running the Application
1. Download the `smart_task_manager.py` file
2. Open a terminal/command prompt
3. Navigate to the file location
4. Run: `python smart_task_manager.py`

## Usage Guide

### Adding Tasks
1. Fill in the task details in the "Add New Task" section:
   - **Title**: Required task name
   - **Description**: Optional detailed description
   - **Deadline**: Optional deadline in YYYY-MM-DD HH:MM format
   - **Urgency**: Scale of 1-10 (10 being most urgent)
   - **Dependencies**: Comma-separated task IDs that must be completed first

2. Click "Add Task" to add the task to your list
3. Tasks automatically appear in the priority-sorted list

### Managing Tasks
- **Complete Task**: Select a task and click "Complete Task"
- **Delete Task**: Select a task and click "Delete Task"
- **View Details**: Double-click any task to see detailed information
- **Filter View**: Use "Show Completed" checkbox to toggle completed tasks

### Priority Scoring Algorithm
Tasks are automatically scored based on:
- **Base Score**: Urgency level × 10 (10-100 points)
- **Deadline Score**: 
  - Overdue tasks: +200 points
  - Due today: +100 points
  - Due within 3 days: 80-20 points
  - Due within 7 days: 40-5 points
- **Age Score**: Older tasks get slight priority boost (max +20 points)

### Dependency Management
- Tasks with dependencies are automatically ordered after their prerequisites
- Uses topological sorting to handle complex dependency chains
- Prevents circular dependencies
- Dependencies are automatically removed when tasks are deleted

### Color Coding
- **Red Background**: Overdue tasks
- **Orange Background**: Tasks due within 24 hours
- **Yellow Background**: High urgency tasks (8-10)
- **Green Checkmark**: Completed tasks

### File Operations
- **Save JSON**: Save all tasks to a JSON file for backup
- **Load JSON**: Load previously saved tasks from JSON file
- **Export CSV**: Export task data to CSV for analysis in Excel or other tools

## Technical Implementation

### Architecture
- **Task Class**: Represents individual tasks with priority calculation
- **TaskManager Class**: Manages task collection with priority scheduling
- **SmartTaskManagerGUI Class**: Tkinter-based user interface

### Priority Scheduling Algorithm
- Combines urgency, deadline proximity, and task age
- Uses topological sorting for dependency resolution
- Implements heap-based priority queue for efficient sorting

### Data Structures
- Dictionary-based task storage for O(1) lookup
- Heap queue for priority management
- Dependency graph for topological sorting

## Development Notes

### Key Algorithms Implemented
1. **Priority Calculation**: Multi-factor scoring system
2. **Topological Sort**: Dependency-aware task ordering
3. **Real-time Updates**: Dynamic priority recalculation

### Design Patterns Used
- **Model-View-Controller**: Separation of data, logic, and UI
- **Observer Pattern**: Real-time UI updates
- **Factory Pattern**: Task creation and serialization

## License
This software is provided as-is for educational and productivity purposes.

## Support
For issues or questions, please refer to the code comments or modify the source as needed.
