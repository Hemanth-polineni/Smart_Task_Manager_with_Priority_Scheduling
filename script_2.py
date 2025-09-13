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

print("GUI setup methods complete!")