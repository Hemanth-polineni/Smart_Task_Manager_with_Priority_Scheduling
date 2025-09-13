# Continue with task management methods
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

# Add these methods to the SmartTaskManagerGUI class
SmartTaskManagerGUI.clear_fields = clear_fields
SmartTaskManagerGUI.parse_deadline = parse_deadline
SmartTaskManagerGUI.parse_dependencies = parse_dependencies
SmartTaskManagerGUI.add_task = add_task
SmartTaskManagerGUI.complete_task = complete_task
SmartTaskManagerGUI.delete_task = delete_task
SmartTaskManagerGUI.on_task_double_click = on_task_double_click

print("Task management methods complete!")