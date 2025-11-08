"""
Admin GUI for Horse Racing Database System
Handles all administrative functions for the system
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database

class AdminGUI:
    def __init__(self, root, db_manager, back_callback):
        self.root = root
        self.db_manager = db_manager
        self.back_callback = back_callback
        self.root.title("Admin Panel - Horse Racing Database")
        self.root.geometry("800x600")
        self.root.configure(bg="#34495E")
        
        self.create_admin_interface()
        
    def create_admin_interface(self):
        """Create the main admin interface with tabs"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2C3E50")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Admin Panel",
            font=("Arial", 20, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        back_button = tk.Button(
            header_frame,
            text="Back to Main",
            font=("Arial", 10),
            bg="#E74C3C",
            fg="white",
            command=self.back_to_main
        )
        back_button.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs
        self.create_add_race_tab()
        self.create_delete_owner_tab()
        self.create_move_horse_tab()
        self.create_approve_trainer_tab()
        
    def create_add_race_tab(self):
        """Create tab for adding new races"""
        race_frame = ttk.Frame(self.notebook)
        self.notebook.add(race_frame, text="Add Race")
        
        # Title
        title_label = tk.Label(
            race_frame,
            text="Add New Race with Results",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Race info frame
        info_frame = tk.Frame(race_frame, bg="#34495E")
        info_frame.pack(pady=20)
        
        # Race details
        tk.Label(info_frame, text="Race Name:", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.race_name_var = tk.StringVar()
        tk.Entry(info_frame, textvariable=self.race_name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(info_frame, text="Track:", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.track_var = tk.StringVar()
        self.track_combo = ttk.Combobox(info_frame, textvariable=self.track_var, state="readonly", width=28)
        self.track_combo.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(info_frame, text="Race Date (YYYY-MM-DD):", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.race_date_var = tk.StringVar()
        tk.Entry(info_frame, textvariable=self.race_date_var, width=30).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(info_frame, text="Race Time (HH:MM:SS):", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.race_time_var = tk.StringVar()
        tk.Entry(info_frame, textvariable=self.race_time_var, width=30).grid(row=3, column=1, padx=10, pady=5)
        
        # Load tracks into combo box
        self.load_tracks()
        
        # Results frame
        results_frame = tk.Frame(race_frame, bg="#34495E")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        tk.Label(results_frame, text="Race Results:", bg="#34495E", fg="white", font=("Arial", 12, "bold")).pack()
        
        # Results listbox
        listbox_frame = tk.Frame(results_frame, bg="#34495E")
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.results_listbox = tk.Listbox(listbox_frame, font=("Arial", 10))
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.results_listbox.yview)
        self.results_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(race_frame, bg="#34495E")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Add Result", command=self.add_result, bg="#27AE60", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Remove Result", command=self.remove_result, bg="#E67E22", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Save Race", command=self.save_race, bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Results data
        self.results_data = []
        
    def create_delete_owner_tab(self):
        """Create tab for deleting owners"""
        delete_frame = ttk.Frame(self.notebook)
        self.notebook.add(delete_frame, text="Delete Owner")
        
        # Title
        title_label = tk.Label(
            delete_frame,
            text="Delete Owner (Using Stored Procedure)",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Owner selection frame
        selection_frame = tk.Frame(delete_frame, bg="#34495E")
        selection_frame.pack(pady=20)
        
        tk.Label(selection_frame, text="Select Owner to Delete:", bg="#34495E", fg="white", font=("Arial", 12)).pack()
        
        # Owner listbox
        listbox_frame = tk.Frame(selection_frame, bg="#34495E")
        listbox_frame.pack(pady=10)
        
        self.owner_listbox = tk.Listbox(listbox_frame, font=("Arial", 10), width=50)
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.owner_listbox.yview)
        self.owner_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.owner_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load owners
        self.load_owners()
        
        # Button
        tk.Button(selection_frame, text="Delete Selected Owner", command=self.delete_owner, 
                 bg="#E74C3C", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        
    def create_move_horse_tab(self):
        """Create tab for moving horses between stables"""
        move_frame = ttk.Frame(self.notebook)
        self.notebook.add(move_frame, text="Move Horse")
        
        # Title
        title_label = tk.Label(
            move_frame,
            text="Move Horse to Different Stable",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Move details frame
        move_details_frame = tk.Frame(move_frame, bg="#34495E")
        move_details_frame.pack(pady=20)
        
        tk.Label(move_details_frame, text="Horse ID:", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.horse_id_var = tk.StringVar()
        tk.Entry(move_details_frame, textvariable=self.horse_id_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(move_details_frame, text="Current Stable:", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.current_stable_var = tk.StringVar()
        tk.Label(move_details_frame, textvariable=self.current_stable_var, bg="#34495E", fg="#3498DB", font=("Arial", 10, "bold")).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(move_details_frame, text="New Stable:", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.new_stable_var = tk.StringVar()
        self.move_stable_combo = ttk.Combobox(move_details_frame, textvariable=self.new_stable_var, state="readonly", width=28)
        self.move_stable_combo.grid(row=2, column=1, padx=10, pady=5)
        
        # Load stables for this combobox
        try:
            stables = self.db_manager.execute_query("SELECT stableId, stableName FROM Stable ORDER BY stableName")
            if stables:
                stable_names = [f"{stable['stableId']}: {stable['stableName']}" for stable in stables]
                self.move_stable_combo['values'] = stable_names
        except Exception as e:
            print(f"Error loading stables for move horse tab: {e}")
        
        # Buttons
        button_frame = tk.Frame(move_frame, bg="#34495E")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Check Horse Info", command=self.check_horse_info, bg="#F39C12", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Move Horse", command=self.move_horse, bg="#27AE60", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Info frame
        info_frame = tk.Frame(move_frame, bg="#34495E")
        info_frame.pack(fill=tk.X, pady=20)
        
        self.horse_info_label = tk.Label(info_frame, text="", bg="#34495E", fg="white", font=("Arial", 10), wraplength=500)
        self.horse_info_label.pack()
        
    def create_approve_trainer_tab(self):
        """Create tab for approving new trainers"""
        try:
            trainer_frame = ttk.Frame(self.notebook)
            self.notebook.add(trainer_frame, text="Approve Trainer")
            
            # Title
            title_label = tk.Label(
                trainer_frame,
                text="Approve New Trainer",
                font=("Arial", 16, "bold"),
                bg="#34495E",
                fg="white"
            )
            title_label.pack(pady=20)
            
            # Trainer details frame
            details_frame = tk.Frame(trainer_frame, bg="#34495E")
            details_frame.pack(pady=20)
            
            tk.Label(details_frame, text="First Name:", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
            self.trainer_fname_var = tk.StringVar()
            tk.Entry(details_frame, textvariable=self.trainer_fname_var, width=30).grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(details_frame, text="Last Name:", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
            self.trainer_lname_var = tk.StringVar()
            tk.Entry(details_frame, textvariable=self.trainer_lname_var, width=30).grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(details_frame, text="Assign to Stable:", bg="#34495E", fg="white", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
            self.trainer_stable_var = tk.StringVar()
            self.trainer_stable_combo = ttk.Combobox(details_frame, textvariable=self.trainer_stable_var, state="readonly", width=28)
            self.trainer_stable_combo.grid(row=2, column=1, padx=10, pady=5)
            
            # Load stables for this combobox
            try:
                stables = self.db_manager.execute_query("SELECT stableId, stableName FROM Stable ORDER BY stableName")
                if stables:
                    stable_names = [f"{stable['stableId']}: {stable['stableName']}" for stable in stables]
                    self.trainer_stable_combo['values'] = stable_names
            except Exception as e:
                print(f"Error loading stables for trainer tab: {e}")
            
            # Button
            tk.Button(trainer_frame, text="Approve Trainer", command=self.approve_trainer, 
                     bg="#27AE60", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        except Exception as e:
            print(f"Error creating approve trainer tab: {e}")
            messagebox.showerror("Error", f"Failed to create Approve Trainer tab: {e}")
        
    def load_tracks(self):
        """Load available tracks"""
        try:
            tracks = self.db_manager.execute_query("SELECT trackName FROM Track ORDER BY trackName")
            if tracks:
                track_names = [track['trackName'] for track in tracks]
                self.track_combo['values'] = track_names
                if track_names:
                    self.track_combo.current(0)  # Select first track by default
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tracks: {e}")
    
    def convert_position_to_text(self, position):
        """Convert numeric position to text format for database consistency"""
        position_map = {
            1: 'first',
            2: 'second',
            3: 'third',
            4: 'fourth',
            5: 'fifth',
            6: 'sixth',
            7: 'seventh',
            8: 'eighth',
            9: 'ninth',
            10: 'tenth'
        }
        return position_map.get(position, str(position))
    
    def load_owners(self):
        """Load owners for deletion"""
        try:
            owners = self.db_manager.execute_query("""
                SELECT ownerId, CONCAT(fname, ' ', lname) as full_name 
                FROM Owner ORDER BY lname, fname
            """)
            if owners:
                self.owner_listbox.delete(0, tk.END)
                for owner in owners:
                    self.owner_listbox.insert(tk.END, f"{owner['ownerId']}: {owner['full_name']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load owners: {e}")
    
    def load_stables(self):
        """Load stables for selection - kept for compatibility but not actively used"""
        pass
    
    def add_result(self):
        """Add a race result"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Add Race Result")
        result_window.geometry("400x300")
        result_window.configure(bg="#34495E")
        
        tk.Label(result_window, text="Add Race Result", font=("Arial", 14, "bold"), 
                bg="#34495E", fg="white").pack(pady=10)
        
        # Result details frame
        details_frame = tk.Frame(result_window, bg="#34495E")
        details_frame.pack(pady=20)
        
        # Result details
        tk.Label(details_frame, text="Horse ID:", bg="#34495E", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5, padx=10)
        horse_id_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=horse_id_var, width=20).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(details_frame, text="Final Position:", bg="#34495E", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
        position_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=position_var, width=20).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(details_frame, text="Prize Money:", bg="#34495E", fg="white").grid(row=2, column=0, sticky=tk.W, pady=5, padx=10)
        prize_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=prize_var, width=20).grid(row=2, column=1, padx=10, pady=5)
        
        def save_result():
            try:
                horse_id = horse_id_var.get().strip()
                position = int(position_var.get())
                prize = float(prize_var.get())
                
                if not horse_id:
                    messagebox.showerror("Error", "Please enter a horse ID")
                    return
                
                # Verify the horse exists
                horse_info = self.db_manager.execute_query("SELECT horseName FROM Horse WHERE horseId = %s", (horse_id,))
                if not horse_info:
                    messagebox.showerror("Error", f"Horse with ID '{horse_id}' not found")
                    return
                
                # Convert numeric position to text format for database consistency
                position_text = self.convert_position_to_text(position)
                
                self.results_data.append({
                    'horseId': horse_id,
                    'position': position_text,
                    'prize': prize
                })
                
                # Add to listbox
                horse_name = horse_info[0]['horseName']
                self.results_listbox.insert(tk.END, f"Position {position}: {horse_name} (Horse ID: {horse_id}) - ${prize:,.2f}")
                
                result_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Error", "Please enter valid numbers for position and prize")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add result: {e}")
        
        tk.Button(result_window, text="Save Result", command=save_result, bg="#27AE60", fg="white", 
                 font=("Arial", 10, "bold")).pack(pady=20)
    
    def remove_result(self):
        """Remove selected result"""
        try:
            selection = self.results_listbox.curselection()
            if selection:
                index = selection[0]
                self.results_listbox.delete(index)
                del self.results_data[index]
        except tk.TclError:
            pass
    
    def save_race(self):
        """Save the race with results"""
        try:
            # Validate inputs
            race_name = self.race_name_var.get().strip()
            track_name = self.track_var.get().strip()
            race_date = self.race_date_var.get().strip()
            race_time = self.race_time_var.get().strip()
            
            if not all([race_name, track_name, race_date, race_time]):
                messagebox.showerror("Error", "All race fields are required")
                return
            
            if not self.results_data:
                messagebox.showerror("Error", "Please add at least one race result")
                return
            
            # Generate a unique race ID
            import time
            race_id = f"race{int(time.time()) % 100000}"
            
            # Insert race
            query = """
                INSERT INTO Race (raceId, raceName, trackName, raceDate, raceTime) 
                VALUES (%s, %s, %s, %s, %s)
            """
            result = self.db_manager.execute_query(query, (race_id, race_name, track_name, race_date, race_time))
            
            if result is not None:
                # Insert results
                for result_data in self.results_data:
                    query = """
                        INSERT INTO RaceResults (raceId, horseId, results, prize) 
                        VALUES (%s, %s, %s, %s)
                    """
                    self.db_manager.execute_query(query, (
                        race_id, 
                        result_data['horseId'], 
                        result_data['position'], 
                        result_data['prize']
                    ))
                
                messagebox.showinfo("Success", f"Race added successfully! Race ID: {race_id}")
                
                # Clear form
                self.race_name_var.set("")
                self.track_var.set("")
                self.race_date_var.set("")
                self.race_time_var.set("")
                self.results_listbox.delete(0, tk.END)
                self.results_data = []
            else:
                messagebox.showerror("Error", "Failed to add race")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save race: {e}")
    
    def delete_owner(self):
        """Delete selected owner using stored procedure"""
        try:
            selection = self.owner_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select an owner to delete")
                return
            
            owner_text = self.owner_listbox.get(selection[0])
            owner_id = owner_text.split(':')[0].strip()  # Extract and clean the owner ID
            
            # Confirm deletion
            if messagebox.askyesno("Confirm", f"Are you sure you want to delete owner {owner_id}? This will also remove all ownership relationships. This action cannot be undone."):
                # Call stored procedure
                result = self.db_manager.execute_procedure("DeleteOwner", [owner_id])
                
                messagebox.showinfo("Success", f"Owner {owner_id} deleted successfully!")
                self.load_owners()  # Refresh the list
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete owner: {e}")
    
    def check_horse_info(self):
        """Check horse information"""
        try:
            horse_id = self.horse_id_var.get().strip()
            
            if not horse_id:
                messagebox.showerror("Error", "Please enter a horse ID")
                return
            
            horse_info = self.db_manager.execute_query("""
                SELECT h.horseName, h.age, h.gender, s.stableName
                FROM Horse h
                LEFT JOIN Stable s ON h.stableId = s.stableId
                WHERE h.horseId = %s
            """, (horse_id,))
            
            if horse_info:
                horse = horse_info[0]
                self.current_stable_var.set(horse['stableName'] or 'No Stable')
                self.horse_info_label.config(text=f"Name: {horse['horseName']}, Age: {horse['age']}, Gender: {horse['gender']}")
            else:
                messagebox.showerror("Error", "Horse not found")
                self.current_stable_var.set("")
                self.horse_info_label.config(text="")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get horse info: {e}")
    
    def move_horse(self):
        """Move horse to new stable"""
        try:
            horse_id = self.horse_id_var.get().strip()
            new_stable_text = self.new_stable_var.get().strip()
            
            if not horse_id:
                messagebox.showerror("Error", "Please enter a horse ID")
                return
            
            if not new_stable_text:
                messagebox.showerror("Error", "Please select a new stable")
                return
            
            # Extract stable ID from the combobox text (format: "stableId: stableName")
            new_stable_id = new_stable_text.split(':')[0].strip()
            
            # Verify the horse exists first
            horse_check = self.db_manager.execute_query("SELECT horseId FROM Horse WHERE horseId = %s", (horse_id,))
            if not horse_check:
                messagebox.showerror("Error", f"Horse with ID '{horse_id}' not found")
                return
            
            # Update horse stable
            query = "UPDATE Horse SET stableId = %s WHERE horseId = %s"
            result = self.db_manager.execute_query(query, (new_stable_id, horse_id))
            
            if result is not None and result > 0:
                messagebox.showinfo("Success", f"Horse {horse_id} moved to stable {new_stable_id} successfully!")
                self.check_horse_info()  # Refresh info
            else:
                messagebox.showerror("Error", "Failed to move horse")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move horse: {e}")
    
    def approve_trainer(self):
        """Approve new trainer"""
        try:
            fname = self.trainer_fname_var.get().strip()
            lname = self.trainer_lname_var.get().strip()
            stable_text = self.trainer_stable_var.get().strip()
            
            if not fname or not lname:
                messagebox.showerror("Error", "First name and last name are required")
                return
            
            if not stable_text:
                messagebox.showerror("Error", "Please select a stable")
                return
            
            # Extract stable ID from the combobox text (format: "stableId: stableName")
            stable_id = stable_text.split(':')[0].strip()
            
            # Generate a unique trainer ID using timestamp
            import time
            trainer_id = f"T{int(time.time()) % 100000}"
            
            # Insert new trainer
            query = "INSERT INTO Trainer (trainerId, fname, lname, stableId) VALUES (%s, %s, %s, %s)"
            result = self.db_manager.execute_query(query, (trainer_id, fname, lname, stable_id))
            
            if result is not None and result > 0:
                messagebox.showinfo("Success", f"Trainer {fname} {lname} approved successfully!\nTrainer ID: {trainer_id}\nAssigned to Stable: {stable_id}")
                # Clear form
                self.trainer_fname_var.set("")
                self.trainer_lname_var.set("")
                self.trainer_stable_var.set("")
            else:
                messagebox.showerror("Error", "Failed to approve trainer")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve trainer: {e}")
    
    def back_to_main(self):
        """Return to main menu"""
        self.root.destroy()
        self.back_callback()