    def update_time(self):
        """Update the current time display."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.master.after(1000, self.update_time)  # Update every second
    
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

# Add these methods to the SmartTaskManagerGUI class
SmartTaskManagerGUI.update_time = update_time
SmartTaskManagerGUI.clear_fields = clear_fields
SmartTaskManagerGUI.parse_deadline = parse_deadline
SmartTaskManagerGUI.parse_dependencies = parse_dependencies
SmartTaskManagerGUI.add_task = add_task
SmartTaskManagerGUI.complete_task = complete_task
SmartTaskManagerGUI.delete_task = delete_task
SmartTaskManagerGUI.on_task_double_click = on_task_double_click
SmartTaskManagerGUI.show_task_details = show_task_details
SmartTaskManagerGUI.refresh_task_list = refresh_task_list
SmartTaskManagerGUI.update_statistics = update_statistics
SmartTaskManagerGUI.update_status = update_status
SmartTaskManagerGUI.save_tasks = save_tasks
SmartTaskManagerGUI.load_tasks = load_tasks
SmartTaskManagerGUI.export_csv = export_csv
SmartTaskManagerGUI.load_default_data = load_default_data

print("GUI methods implementation complete!")