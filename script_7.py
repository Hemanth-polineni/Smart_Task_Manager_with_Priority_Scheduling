# Continue with display and utility methods
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

# Add these methods to the SmartTaskManagerGUI class
SmartTaskManagerGUI.show_task_details = show_task_details
SmartTaskManagerGUI.refresh_task_list = refresh_task_list
SmartTaskManagerGUI.update_statistics = update_statistics
SmartTaskManagerGUI.update_status = update_status

print("Display and utility methods complete!")