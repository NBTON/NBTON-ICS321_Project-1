"""
Main GUI application for Horse Racing Database System
Handles user type selection and navigation to appropriate interfaces
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database
from admin_gui import AdminGUI
from guest_gui import GuestGUI

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Horse Racing Database System")
        self.root.geometry("600x400")
        self.root.configure(bg="#2C3E50")
        
        # Store database manager reference
        self.db_manager = database.db_manager
        
        # Create main interface
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create the main login/selection interface"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Horse Racing Database System",
            font=("Arial", 24, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.pack(pady=50)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Select Your User Type",
            font=("Arial", 16),
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        subtitle_label.pack(pady=10)
        
        # User type selection frame
        selection_frame = tk.Frame(self.root, bg="#2C3E50")
        selection_frame.pack(pady=30)
        
        # Admin button
        admin_button = tk.Button(
            selection_frame,
            text="Admin Access",
            font=("Arial", 14, "bold"),
            bg="#E74C3C",
            fg="white",
            width=15,
            height=2,
            command=self.admin_login
        )
        admin_button.pack(side=tk.LEFT, padx=20)
        
        # Guest button
        guest_button = tk.Button(
            selection_frame,
            text="Guest Access",
            font=("Arial", 14, "bold"),
            bg="#3498DB",
            fg="white",
            width=15,
            height=2,
            command=self.guest_login
        )
        guest_button.pack(side=tk.LEFT, padx=20)
        
        # Setup database button
        setup_frame = tk.Frame(self.root, bg="#2C3E50")
        setup_frame.pack(pady=50)
        
        setup_label = tk.Label(
            setup_frame,
            text="First time setup?",
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#95A5A6"
        )
        setup_label.pack()
        
        setup_button = tk.Button(
            setup_frame,
            text="Setup Database",
            font=("Arial", 10),
            bg="#27AE60",
            fg="white",
            command=self.setup_database
        )
        setup_button.pack()
        
        # Database connection status
        self.status_frame = tk.Frame(self.root, bg="#2C3E50")
        self.status_frame.pack(pady=20)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Database connection: Not tested",
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#F39C12"
        )
        self.status_label.pack()
        
        # Test connection button
        test_button = tk.Button(
            self.status_frame,
            text="Test Database Connection",
            font=("Arial", 9),
            bg="#8E44AD",
            fg="white",
            command=self.test_connection
        )
        test_button.pack(pady=5)
        
    def test_connection(self):
        """Test database connection"""
        if self.db_manager.test_connection():
            self.status_label.config(text="Database connection: Connected", fg="#27AE60")
            messagebox.showinfo("Success", "Database connection successful!")
        else:
            self.status_label.config(text="Database connection: Failed", fg="#E74C3C")
            messagebox.showerror("Error", "Failed to connect to database. Please check MySQL server and configuration.")
    
    def setup_database(self):
        """Setup the database with schema and sample data"""
        # First test connection
        if not self.db_manager.test_connection():
            messagebox.showerror("Error", "Cannot connect to database. Please ensure MySQL server is running.")
            return
        
        # Since the "Horses" database already exists according to MCP config,
        # we'll just run the schema and data setup
        try:
            success = self.db_manager.setup_database()
            if success:
                messagebox.showinfo("Success", "Database setup completed successfully!")
                self.status_label.config(text="Database connection: Connected", fg="#27AE60")
            else:
                messagebox.showerror("Error", "Failed to setup database.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database setup failed: {e}")
    
    def admin_login(self):
        """Handle admin login"""
        self.root.withdraw()  # Hide main window
        admin_window = tk.Toplevel()
        admin_gui = AdminGUI(admin_window, self.db_manager, self.back_to_main)
        
    def guest_login(self):
        """Handle guest login"""
        self.root.withdraw()  # Hide main window
        guest_window = tk.Toplevel()
        guest_gui = GuestGUI(guest_window, self.db_manager, self.back_to_main)
        
    def back_to_main(self):
        """Return to main window"""
        self.root.deiconify()  # Show main window again

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()