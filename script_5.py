# Continue with the rest of the GUI methods
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

# Add these methods to the SmartTaskManagerGUI class
SmartTaskManagerGUI.create_task_list_frame = create_task_list_frame
SmartTaskManagerGUI.create_control_frame = create_control_frame
SmartTaskManagerGUI.create_status_frame = create_status_frame

print("GUI methods - Part 2 complete!")