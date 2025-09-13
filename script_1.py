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
                    if not task_dict[dep_id].completed:
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

print("TaskManager class implementation complete!")