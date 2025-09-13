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

print("Task class implementation complete!")