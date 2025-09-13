#!/usr/bin/env python3
"""
Smart Task Manager with Priority Scheduling
A productivity tool that automatically reorders tasks based on urgency, dependencies, and deadlines.

Author: AI Assistant
Date: 2025
Tech Stack: Python + Tkinter GUI
Algorithm: Smart priority scheduling with topological sorting for dependencies
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import heapq

class Task:
    """Task data structure with priority and dependency management."""

    def __init__(self, task_id: int, title: str, description: str = "", 
                 deadline: Optional[datetime] = None, urgency: int = 5, 
                 dependencies: Optional[List[int]] = None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.urgency = urgency  # 1-10 scale
        self.dependencies = dependencies or []
        self.completed = False
        self.created_at = datetime.now()
        self.priority_score = 0.0

    def calculate_priority_score(self) -> float:
        """Calculate priority score based on deadline urgency and task urgency."""
        base_score = self.urgency * 10  # Base score from urgency (10-100)

        # Deadline component (higher score for closer deadlines)
        deadline_score = 0
        if self.deadline:
            days_until_deadline = (self.deadline - datetime.now()).days
            if days_until_deadline < 0:  # Overdue
                deadline_score = 200  # High penalty for overdue
            elif days_until_deadline == 0:  # Due today
                deadline_score = 100
            elif days_until_deadline <= 3:  # Due within 3 days
                deadline_score = 80 - (days_until_deadline * 20)
            elif days_until_deadline <= 7:  # Due within a week
                deadline_score = 40 - (days_until_deadline * 5)
            else:  # More than a week
                deadline_score = max(0, 20 - days_until_deadline)

        # Age component (older tasks get slight priority boost)
        age_days = (datetime.now() - self.created_at).days
        age_score = min(20, age_days * 2)  # Max 20 points for age

        self.priority_score = base_score + deadline_score + age_score
        return self.priority_score

    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'urgency': self.urgency,
            'dependencies': self.dependencies,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'priority_score': self.priority_score
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary (JSON deserialization)."""
        task = cls(
            task_id=data['task_id'],
            title=data['title'],
            description=data.get('description', ''),
            deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
            urgency=data.get('urgency', 5),
            dependencies=data.get('dependencies', [])
        )
        task.completed = data.get('completed', False)
        task.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        task.priority_score = data.get('priority_score', 0.0)
        return task

class TaskManager:
    """Core task management with priority scheduling and dependency handling."""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1
        self.priority_queue = []  # Min-heap for priority queue

    def add_task(self, title: str, description: str = "", deadline: Optional[datetime] = None, 
                 urgency: int = 5, dependencies: Optional[List[int]] = None) -> int:
        """Add a new task and return its ID."""
        task = Task(self.next_id, title, description, deadline, urgency, dependencies)
        self.tasks[self.next_id] = task
        self.next_id += 1
        self._update_priorities()
        return task.task_id

    def edit_task(self, task_id: int, title: Optional[str] = None, 
                  description: Optional[str] = None, deadline: Optional[datetime] = None,
                  urgency: Optional[int] = None, dependencies: Optional[List[int]] = None) -> bool:
        """Edit an existing task."""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if deadline is not None:
            task.deadline = deadline
        if urgency is not None:
            task.urgency = urgency
        if dependencies is not None:
            task.dependencies = dependencies

        self._update_priorities()
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        if task_id not in self.tasks:
            return False

        # Remove this task as a dependency from other tasks
        for task in self.tasks.values():
            if task_id in task.dependencies:
                task.dependencies.remove(task_id)

        del self.tasks[task_id]
        self._update_priorities()
        return True

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        if task_id not in self.tasks:
            return False

        self.tasks[task_id].completed = True
        self._update_priorities()
        return True

    def get_sorted_tasks(self, include_completed: bool = False) -> List[Task]:
        """Get tasks sorted by priority score (highest first)."""
        tasks = list(self.tasks.values())
        if not include_completed:
            tasks = [t for t in tasks if not t.completed]

        # Update priority scores before sorting
        for task in tasks:
            task.calculate_priority_score()

        # Sort by priority score (descending) and handle dependencies
        sorted_tasks = self._topological_sort_with_priority(tasks)
        return sorted_tasks

    def _topological_sort_with_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks considering both priority and dependencies."""
        # Create a dependency graph
        task_dict = {t.task_id: t for t in tasks}
        in_degree = {t.task_id: 0 for t in tasks}

        # Calculate in-degrees
        for task in tasks:
            for dep_id in task.dependencies:
                if dep_id in in_degree:  # Only count dependencies that exist and aren't completed
                    if dep_id in task_dict and not task_dict[dep_id].completed:
                        in_degree[task.task_id] += 1

        # Use a max-heap (negate priority scores for min-heap)
        available_tasks = []
        for task in tasks:
            if in_degree[task.task_id] == 0:
                heapq.heappush(available_tasks, (-task.priority_score, task.task_id, task))

        sorted_tasks = []

        while available_tasks:
            # Get the highest priority task with no dependencies
            _, task_id, task = heapq.heappop(available_tasks)
            sorted_tasks.append(task)

            # Update in-degrees for dependent tasks
            for other_task in tasks:
                if task_id in other_task.dependencies and not other_task.completed:
                    in_degree[other_task.task_id] -= 1
                    if in_degree[other_task.task_id] == 0:
                        heapq.heappush(available_tasks, (-other_task.priority_score, other_task.task_id, other_task))

        # Add any remaining tasks (in case of cycles)
        remaining_tasks = [t for t in tasks if t not in sorted_tasks]
        remaining_tasks.sort(key=lambda x: -x.priority_score)
        sorted_tasks.extend(remaining_tasks)

        return sorted_tasks

    def _update_priorities(self):
        """Update priority scores for all tasks."""
        for task in self.tasks.values():
            task.calculate_priority_score()

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks."""
        now = datetime.now()
        return [task for task in self.tasks.values() 
                if task.deadline and task.deadline < now and not task.completed]

    def get_tasks_due_today(self) -> List[Task]:
        """Get tasks due today."""
        today = datetime.now().date()
        return [task for task in self.tasks.values()
                if task.deadline and task.deadline.date() == today and not task.completed]

    def get_high_priority_tasks(self) -> List[Task]:
        """Get tasks with urgency >= 8."""
        return [task for task in self.tasks.values() 
                if task.urgency >= 8 and not task.completed]

    def save_to_json(self, filename: str):
        """Save tasks to JSON file."""
        data = {
            'tasks': [task.to_dict() for task in self.tasks.values()],
            'next_id': self.next_id
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_json(self, filename: str):
        """Load tasks from JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.tasks = {}
            for task_data in data.get('tasks', []):
                task = Task.from_dict(task_data)
                self.tasks[task.task_id] = task

            self.next_id = data.get('next_id', 1)
            self._update_priorities()
            return True
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return False

    def export_to_csv(self, filename: str):
        """Export tasks to CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Description', 'Deadline', 'Urgency', 
                           'Dependencies', 'Completed', 'Priority Score'])

            for task in self.tasks.values():
                writer.writerow([
                    task.task_id,
                    task.title,
                    task.description,
                    task.deadline.isoformat() if task.deadline else '',
                    task.urgency,
                    ';'.join(map(str, task.dependencies)) if task.dependencies else '',
                    task.completed,
                    round(task.priority_score, 2)
                ])

class SmartTaskManagerGUI:
    """Tkinter GUI for the Smart Task Manager."""

    def __init__(self, master):
        self.master = master
        self.task_manager = TaskManager()

        # Configure main window
        self.master.title("Smart Task Manager with Priority Scheduling")
        self.master.geometry("1000x700")
        self.master.configure(bg='#f0f0f0')

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Color scheme
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }

        self.setup_gui()
        self.load_default_data()

    def setup_gui(self):
        """Set up the GUI layout."""
        # Create main frames
        self.create_header_frame()
        self.create_input_frame()
        self.create_task_list_frame()
        self.create_control_frame()
        self.create_status_frame()

    def create_header_frame(self):
        """Create header with title and current time."""
        header_frame = tk.Frame(self.master, bg=self.colors['primary'], height=60)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            header_frame,
            text="Smart Task Manager",
            font=('Arial', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Current time
        self.time_label = tk.Label(
            header_frame,
            text="",
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white'
        )
        self.time_label.pack(side=tk.RIGHT, padx=20, pady=15)
        self.update_time()

    def update_time(self):
        """Update the current time display."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.master.after(1000, self.update_time)  # Update every second

    def create_input_frame(self):
        """Create input fields for adding new tasks."""
        input_frame = tk.LabelFrame(
            self.master,
            text="Add New Task",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        )
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # First row - Title and Urgency
        row1 = tk.Frame(input_frame, bg=self.colors['bg'])
        row1.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(row1, text="Title:", bg=self.colors['bg'], font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.title_entry = tk.Entry(row1, font=('Arial', 10), width=30)
        self.title_entry.pack(side=tk.LEFT, padx=(5, 20))

        tk.Label(row1, text="Urgency (1-10):", bg=self.colors['bg'], font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.urgency_var = tk.StringVar(value="5")
        urgency_combo = ttk.Combobox(row1, textvariable=self.urgency_var, values=list(map(str, range(1, 11))), width=5)
        urgency_combo.pack(side=tk.LEFT, padx=5)

        # Second row - Description
        row2 = tk.Frame(input_frame, bg=self.colors['bg'])
        row2.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(row2, text="Description:", bg=self.colors['bg'], font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.description_text = tk.Text(row2, height=3, font=('Arial', 9), wrap=tk.WORD)
        self.description_text.pack(fill=tk.X, pady=(5, 0))

        # Third row - Deadline and Dependencies
        row3 = tk.Frame(input_frame, bg=self.colors['bg'])
        row3.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(row3, text="Deadline (YYYY-MM-DD HH:MM):", bg=self.colors['bg'], font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.deadline_entry = tk.Entry(row3, font=('Arial', 10), width=20)
        self.deadline_entry.pack(side=tk.LEFT, padx=(5, 20))

        tk.Label(row3, text="Dependencies (IDs):", bg=self.colors['bg'], font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.dependencies_entry = tk.Entry(row3, font=('Arial', 10), width=15)
        self.dependencies_entry.pack(side=tk.LEFT, padx=5)

        # Fourth row - Buttons
        button_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        add_btn = tk.Button(
            button_frame,
            text="Add Task",
            command=self.add_task,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 10))

        clear_btn = tk.Button(
            button_frame,
            text="Clear Fields",
            command=self.clear_fields,
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20
        )
        clear_btn.pack(side=tk.LEFT)

    def create_task_list_frame(self):
        """Create the main task list display."""
        list_frame = tk.LabelFrame(
            self.master,
            text="Task List (Sorted by Priority)",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create Treeview for task list
        columns = ('ID', 'Title', 'Urgency', 'Deadline', 'Priority Score', 'Status', 'Dependencies')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        # Configure columns
        col_widths = {'ID': 50, 'Title': 200, 'Urgency': 70, 'Deadline': 120, 
                      'Priority Score': 100, 'Status': 80, 'Dependencies': 100}

        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=col_widths.get(col, 100))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.task_tree.xview)
        self.task_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack components
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind double-click event
        self.task_tree.bind('<Double-1>', self.on_task_double_click)

    def create_control_frame(self):
        """Create control buttons for task operations."""
        control_frame = tk.Frame(self.master, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Left side - Task operations
        left_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        complete_btn = tk.Button(
            left_frame,
            text="Complete Task",
            command=self.complete_task,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 9, 'bold')
        )
        complete_btn.pack(side=tk.LEFT, padx=(0, 5))

        delete_btn = tk.Button(
            left_frame,
            text="Delete Task",
            command=self.delete_task,
            bg=self.colors['danger'],
            fg='white',
            font=('Arial', 9, 'bold')
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(
            left_frame,
            text="Refresh List",
            command=self.refresh_task_list,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 9, 'bold')
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Filter options
        filter_frame = tk.LabelFrame(left_frame, text="Filters", bg=self.colors['bg'])
        filter_frame.pack(side=tk.LEFT, padx=(20, 0))

        self.show_completed_var = tk.BooleanVar()
        show_completed_cb = tk.Checkbutton(
            filter_frame,
            text="Show Completed",
            variable=self.show_completed_var,
            bg=self.colors['bg'],
            command=self.refresh_task_list
        )
        show_completed_cb.pack(side=tk.LEFT, padx=5)

        # Right side - File operations
        right_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        right_frame.pack(side=tk.RIGHT)

        save_btn = tk.Button(
            right_frame,
            text="Save JSON",
            command=self.save_tasks,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 9, 'bold')
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        load_btn = tk.Button(
            right_frame,
            text="Load JSON",
            command=self.load_tasks,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 9, 'bold')
        )
        load_btn.pack(side=tk.LEFT, padx=5)

        export_btn = tk.Button(
            right_frame,
            text="Export CSV",
            command=self.export_csv,
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 9, 'bold')
        )
        export_btn.pack(side=tk.LEFT, padx=5)

    def create_status_frame(self):
        """Create status bar showing task statistics."""
        status_frame = tk.Frame(self.master, bg=self.colors['dark'], height=30)
        status_frame.pack(fill=tk.X, padx=5, pady=2)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            bg=self.colors['dark'],
            fg='white',
            font=('Arial', 9)
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Task statistics
        self.stats_label = tk.Label(
            status_frame,
            text="",
            bg=self.colors['dark'],
            fg='white',
            font=('Arial', 9)
        )
        self.stats_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def clear_fields(self):
        """Clear all input fields."""
        self.title_entry.delete(0, tk.END)
        self.description_text.delete(1.0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.dependencies_entry.delete(0, tk.END)
        self.urgency_var.set("5")

    def parse_deadline(self, deadline_str: str) -> Optional[datetime]:
        """Parse deadline string to datetime object."""
        if not deadline_str.strip():
            return None

        formats = [
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
            "%m/%d/%Y %H:%M",
            "%m/%d/%Y"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(deadline_str.strip(), fmt)
            except ValueError:
                continue

        raise ValueError(f"Invalid deadline format: {deadline_str}")

    def parse_dependencies(self, deps_str: str) -> List[int]:
        """Parse dependencies string to list of task IDs."""
        if not deps_str.strip():
            return []

        try:
            deps = [int(x.strip()) for x in deps_str.split(',') if x.strip()]
            # Validate that dependencies exist
            valid_deps = [dep for dep in deps if dep in self.task_manager.tasks]
            return valid_deps
        except ValueError:
            raise ValueError("Dependencies must be comma-separated task IDs")

    def add_task(self):
        """Add a new task from input fields."""
        try:
            title = self.title_entry.get().strip()
            if not title:
                messagebox.showerror("Error", "Task title is required!")
                return

            description = self.description_text.get(1.0, tk.END).strip()
            urgency = int(self.urgency_var.get())

            deadline = None
            deadline_str = self.deadline_entry.get().strip()
            if deadline_str:
                deadline = self.parse_deadline(deadline_str)

            dependencies = self.parse_dependencies(self.dependencies_entry.get())

            task_id = self.task_manager.add_task(title, description, deadline, urgency, dependencies)
            self.clear_fields()
            self.refresh_task_list()
            self.update_status(f"Added task #{task_id}: {title}")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add task: {e}")

    def complete_task(self):
        """Mark selected task as completed."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to complete.")
            return

        task_id = int(self.task_tree.item(selected_item[0])['values'][0])

        if self.task_manager.complete_task(task_id):
            self.refresh_task_list()
            task = self.task_manager.tasks[task_id]
            self.update_status(f"Completed task #{task_id}: {task.title}")
        else:
            messagebox.showerror("Error", "Failed to complete task.")

    def delete_task(self):
        """Delete selected task."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return

        task_id = int(self.task_tree.item(selected_item[0])['values'][0])
        task = self.task_manager.tasks[task_id]

        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete task #{task_id}: {task.title}?"
        )

        if result:
            if self.task_manager.delete_task(task_id):
                self.refresh_task_list()
                self.update_status(f"Deleted task #{task_id}: {task.title}")
            else:
                messagebox.showerror("Error", "Failed to delete task.")

    def on_task_double_click(self, event):
        """Handle double-click on task (show details)."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return

        task_id = int(self.task_tree.item(selected_item[0])['values'][0])
        task = self.task_manager.tasks[task_id]

        # Create task detail window
        self.show_task_details(task)

    def show_task_details(self, task: Task):
        """Show detailed task information in a popup window."""
        detail_window = tk.Toplevel(self.master)
        detail_window.title(f"Task #{task.task_id} Details")
        detail_window.geometry("500x400")
        detail_window.configure(bg=self.colors['bg'])

        # Title
        title_frame = tk.Frame(detail_window, bg=self.colors['primary'])
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(
            title_frame,
            text=task.title,
            font=('Arial', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=10)

        # Details
        details_frame = tk.Frame(detail_window, bg=self.colors['bg'])
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        details = [
            ("ID:", str(task.task_id)),
            ("Urgency:", f"{task.urgency}/10"),
            ("Priority Score:", f"{task.priority_score:.1f}"),
            ("Status:", "Completed" if task.completed else "Pending"),
            ("Created:", task.created_at.strftime("%Y-%m-%d %H:%M")),
            ("Deadline:", task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "None"),
            ("Dependencies:", ", ".join(map(str, task.dependencies)) if task.dependencies else "None")
        ]

        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(details_frame, bg=self.colors['bg'])
            row_frame.pack(fill=tk.X, pady=5)

            tk.Label(row_frame, text=label, font=('Arial', 10, 'bold'), 
                    bg=self.colors['bg'], width=15, anchor='w').pack(side=tk.LEFT)
            tk.Label(row_frame, text=value, font=('Arial', 10),
                    bg=self.colors['bg'], anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Description
        if task.description:
            desc_frame = tk.LabelFrame(details_frame, text="Description", bg=self.colors['bg'])
            desc_frame.pack(fill=tk.BOTH, expand=True, pady=10)

            desc_text = tk.Text(desc_frame, height=6, wrap=tk.WORD, font=('Arial', 9))
            desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            desc_text.insert(1.0, task.description)
            desc_text.config(state=tk.DISABLED)

    def refresh_task_list(self):
        """Refresh the task list display."""
        # Clear current items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Get sorted tasks
        include_completed = self.show_completed_var.get()
        tasks = self.task_manager.get_sorted_tasks(include_completed)

        # Insert tasks with color coding
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            deadline_str = task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else ""
            deps_str = ", ".join(map(str, task.dependencies)) if task.dependencies else ""

            values = (
                task.task_id,
                task.title[:30] + "..." if len(task.title) > 30 else task.title,
                f"{task.urgency}/10",
                deadline_str,
                f"{task.priority_score:.1f}",
                status,
                deps_str
            )

            item = self.task_tree.insert('', tk.END, values=values)

            # Color coding based on status and urgency
            if task.completed:
                self.task_tree.set(item, 'Status', '✓ Completed')
            elif task.deadline and task.deadline < datetime.now():
                # Overdue - red background
                self.task_tree.item(item, tags=('overdue',))
            elif task.deadline and (task.deadline - datetime.now()).days <= 1:
                # Due soon - orange background
                self.task_tree.item(item, tags=('due_soon',))
            elif task.urgency >= 8:
                # High urgency - yellow background
                self.task_tree.item(item, tags=('high_urgency',))

        # Configure tag colors
        self.task_tree.tag_configure('overdue', background='#ffcccc')
        self.task_tree.tag_configure('due_soon', background='#ffe6cc')
        self.task_tree.tag_configure('high_urgency', background='#ffffcc')

        self.update_statistics()

    def update_statistics(self):
        """Update task statistics display."""
        total_tasks = len([t for t in self.task_manager.tasks.values() if not t.completed])
        completed_tasks = len([t for t in self.task_manager.tasks.values() if t.completed])
        overdue_tasks = len(self.task_manager.get_overdue_tasks())
        high_priority = len(self.task_manager.get_high_priority_tasks())

        stats_text = (f"Total: {total_tasks} | Completed: {completed_tasks} | "
                     f"Overdue: {overdue_tasks} | High Priority: {high_priority}")
        self.stats_label.config(text=stats_text)

    def update_status(self, message: str):
        """Update status bar message."""
        self.status_label.config(text=message)
        self.master.after(3000, lambda: self.status_label.config(text="Ready"))

    def save_tasks(self):
        """Save tasks to JSON file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                self.task_manager.save_to_json(filename)
                self.update_status(f"Tasks saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save tasks: {e}")

    def load_tasks(self):
        """Load tasks from JSON file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                if self.task_manager.load_from_json(filename):
                    self.refresh_task_list()
                    self.update_status(f"Tasks loaded from {filename}")
                else:
                    messagebox.showerror("Error", "Failed to load tasks from file")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")

    def export_csv(self):
        """Export tasks to CSV file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            try:
                self.task_manager.export_to_csv(filename)
                self.update_status(f"Tasks exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export tasks: {e}")

    def load_default_data(self):
        """Load some sample tasks for demonstration."""
        sample_tasks = [
            {
                'title': 'Complete Project Proposal',
                'description': 'Write and submit the final project proposal for Q4 planning.',
                'deadline': datetime.now() + timedelta(days=2),
                'urgency': 9,
                'dependencies': []
            },
            {
                'title': 'Team Meeting Preparation',
                'description': 'Prepare agenda and materials for weekly team meeting.',
                'deadline': datetime.now() + timedelta(days=1),
                'urgency': 7,
                'dependencies': []
            },
            {
                'title': 'Code Review',
                'description': 'Review pull requests from team members.',
                'deadline': datetime.now() + timedelta(hours=4),
                'urgency': 6,
                'dependencies': []
            },
            {
                'title': 'Update Documentation',
                'description': 'Update API documentation with recent changes.',
                'deadline': datetime.now() + timedelta(days=5),
                'urgency': 4,
                'dependencies': [1]  # Depends on first task
            },
            {
                'title': 'Client Presentation',
                'description': 'Prepare presentation for client meeting next week.',
                'deadline': datetime.now() + timedelta(days=7),
                'urgency': 8,
                'dependencies': [1, 4]  # Depends on first and fourth task
            }
        ]

        for task_data in sample_tasks:
            self.task_manager.add_task(**task_data)

        self.refresh_task_list()
        self.update_status("Sample tasks loaded")

def main():
    """Main application entry point."""
    print("Starting Smart Task Manager with Priority Scheduling...")
    print("="*60)
    print("Features:")
    print("• Priority-based task scheduling with automatic reordering")
    print("• Task dependency management")
    print("• Deadline urgency calculation")
    print("• Color-coded task display")
    print("• JSON/CSV persistence")
    print("• Real-time priority updates")
    print("="*60)

    root = tk.Tk()

    # Configure the root window
    root.minsize(800, 600)
    try:
        root.state('zoomed') if root.winfo_screenwidth() > 1200 else root.geometry("1000x700")
    except:
        root.geometry("1000x700")

    # Create the application
    app = SmartTaskManagerGUI(root)

    print("Application initialized successfully!")
    print("Sample tasks have been loaded for demonstration.")
    print("\nInstructions:")
    print("1. Add new tasks using the input form")
    print("2. Tasks are automatically sorted by priority score")
    print("3. Double-click tasks to view details")
    print("4. Use buttons to complete, delete, or refresh tasks")
    print("5. Save/Load tasks using JSON files")
    print("6. Export task data to CSV")
    print("\nRunning application...")

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
