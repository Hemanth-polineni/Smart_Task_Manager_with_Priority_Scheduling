# Complete with file operations and sample data
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

# Add these final methods to the SmartTaskManagerGUI class
SmartTaskManagerGUI.save_tasks = save_tasks
SmartTaskManagerGUI.load_tasks = load_tasks
SmartTaskManagerGUI.export_csv = export_csv
SmartTaskManagerGUI.load_default_data = load_default_data

print("All GUI methods added to class! Ready for main application.")

# Main application runner
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
    root.state('zoomed') if root.winfo_screenwidth() > 1200 else root.geometry("1000x700")
    
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

print("Smart Task Manager application is ready to run!")