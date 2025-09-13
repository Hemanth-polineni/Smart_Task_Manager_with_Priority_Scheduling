# Complete GUI implementation with all methods properly defined
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

print("GUI class updated - Part 1 complete!")