"""
Guest GUI for Horse Racing Database System
Handles all guest browsing and search functions
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database

class GuestGUI:
    def __init__(self, root, db_manager, back_callback):
        self.root = root
        self.db_manager = db_manager
        self.back_callback = back_callback
        self.root.title("Guest Panel - Horse Racing Database")
        self.root.geometry("800x600")
        self.root.configure(bg="#34495E")
        
        self.create_guest_interface()
        
    def create_guest_interface(self):
        """Create the main guest interface with tabs"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2C3E50")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Guest Panel",
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
        self.create_horses_by_owner_tab()
        self.create_winning_trainers_tab()
        self.create_trainer_winnings_tab()
        self.create_tracks_stats_tab()
        
    def create_horses_by_owner_tab(self):
        """Create tab for browsing horses by owner last name"""
        owner_frame = ttk.Frame(self.notebook)
        self.notebook.add(owner_frame, text="Horses by Owner")
        
        # Title
        title_label = tk.Label(
            owner_frame,
            text="Browse Horses by Owner Last Name",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(owner_frame, bg="#34495E")
        search_frame.pack(pady=20)
        
        tk.Label(search_frame, text="Owner Last Name:", bg="#34495E", fg="white", font=("Arial", 12)).pack()
        
        input_frame = tk.Frame(search_frame, bg="#34495E")
        input_frame.pack(pady=10)
        
        self.owner_lname_var = tk.StringVar()
        owner_entry = tk.Entry(input_frame, textvariable=self.owner_lname_var, font=("Arial", 12))
        owner_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(input_frame, text="Search", command=self.search_horses_by_owner, 
                 bg="#3498DB", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        # Results frame
        results_frame = tk.Frame(owner_frame, bg="#34495E")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Treeview for results
        tree_frame = tk.Frame(results_frame, bg="#34495E")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Horse Name", "Age", "Gender", "Trainer")
        self.horses_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.horses_tree.heading(col, text=col)
            self.horses_tree.column(col, width=150)
        
        scrollbar_horses = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.horses_tree.yview)
        self.horses_tree.configure(yscrollcommand=scrollbar_horses.set)
        
        self.horses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_horses.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_winning_trainers_tab(self):
        """Create tab for browsing trainers with first place wins"""
        winners_frame = ttk.Frame(self.notebook)
        self.notebook.add(winners_frame, text="Winning Trainers")
        
        # Title
        title_label = tk.Label(
            winners_frame,
            text="Trainers Who Have Trained Winners (First Place Only)",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(winners_frame, bg="#34495E")
        search_frame.pack(pady=20)
        
        tk.Button(search_frame, text="Show All Winning Trainers", command=self.search_winning_trainers,
                 bg="#3498DB", fg="white", font=("Arial", 12, "bold")).pack()
        
        # Results frame
        results_frame = tk.Frame(winners_frame, bg="#34495E")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Treeview for results
        tree_frame = tk.Frame(results_frame, bg="#34495E")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Trainer Name", "Horse Name", "Race Name", "Track", "Date", "Prize")
        self.winners_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.winners_tree.heading(col, text=col)
            self.winners_tree.column(col, width=120)
        
        scrollbar_winners = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.winners_tree.yview)
        self.winners_tree.configure(yscrollcommand=scrollbar_winners.set)
        
        self.winners_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_winners.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_trainer_winnings_tab(self):
        """Create tab for browsing trainers sorted by total winnings"""
        winnings_frame = ttk.Frame(self.notebook)
        self.notebook.add(winnings_frame, text="Trainer Winnings")
        
        # Title
        title_label = tk.Label(
            winnings_frame,
            text="Trainers with Total Winnings (Sorted by Prize Money)",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(winnings_frame, bg="#34495E")
        search_frame.pack(pady=20)
        
        tk.Button(search_frame, text="Show Trainer Winnings", command=self.search_trainer_winnings,
                 bg="#3498DB", fg="white", font=("Arial", 12, "bold")).pack()
        
        # Results frame
        results_frame = tk.Frame(winnings_frame, bg="#34495E")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Treeview for results
        tree_frame = tk.Frame(results_frame, bg="#34495E")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Trainer Name", "Total Winnings", "Number of Wins", "Stable")
        self.winnings_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.winnings_tree.heading(col, text=col)
            self.winnings_tree.column(col, width=150)
        
        scrollbar_winnings = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.winnings_tree.yview)
        self.winnings_tree.configure(yscrollcommand=scrollbar_winnings.set)
        
        self.winnings_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_winnings.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_tracks_stats_tab(self):
        """Create tab for browsing track statistics"""
        tracks_frame = ttk.Frame(self.notebook)
        self.notebook.add(tracks_frame, text="Track Statistics")
        
        # Title
        title_label = tk.Label(
            tracks_frame,
            text="Track Statistics - Race Count and Total Horses",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(tracks_frame, bg="#34495E")
        search_frame.pack(pady=20)
        
        tk.Button(search_frame, text="Show Track Statistics", command=self.search_track_stats,
                 bg="#3498DB", fg="white", font=("Arial", 12, "bold")).pack()
        
        # Results frame
        results_frame = tk.Frame(tracks_frame, bg="#34495E")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Treeview for results
        tree_frame = tk.Frame(results_frame, bg="#34495E")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Track Name", "Location", "Length", "Number of Races", "Total Horses")
        self.tracks_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tracks_tree.heading(col, text=col)
            self.tracks_tree.column(col, width=120)
        
        scrollbar_tracks = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tracks_tree.yview)
        self.tracks_tree.configure(yscrollcommand=scrollbar_tracks.set)
        
        self.tracks_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tracks.pack(side=tk.RIGHT, fill=tk.Y)
        
    def search_horses_by_owner(self):
        """Search horses by owner last name"""
        try:
            owner_lname = self.owner_lname_var.get().strip()
            
            if not owner_lname:
                messagebox.showwarning("Warning", "Please enter an owner last name")
                return
            
            # Clear existing results
            for item in self.horses_tree.get_children():
                self.horses_tree.delete(item)
            
            query = """
                SELECT DISTINCT h.horseName, h.age, h.gender, 
                       CONCAT(t.fname, ' ', t.lname) as trainer_name
                FROM Horse h
                JOIN Owns o ON h.horseId = o.horseId
                JOIN Owner owner ON o.ownerId = owner.ownerId
                LEFT JOIN Trainer t ON h.stableId = t.stableId
                WHERE owner.lname LIKE %s
                ORDER BY h.horseName
            """
            
            results = self.db_manager.execute_query(query, (f"%{owner_lname}%",))
            
            if results:
                for row in results:
                    self.horses_tree.insert("", tk.END, values=(
                        row['horseName'],
                        row['age'],
                        row['gender'],
                        row['trainer_name'] or 'No Trainer'
                    ))
            else:
                messagebox.showinfo("No Results", f"No horses found for owner with last name '{owner_lname}'")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search horses: {e}")
    
    def search_winning_trainers(self):
        """Search trainers who have trained first place winners"""
        try:
            # Clear existing results
            for item in self.winners_tree.get_children():
                self.winners_tree.delete(item)
            
            query = """
                SELECT DISTINCT CONCAT(t.fname, ' ', t.lname) as trainer_name,
                       h.horseName as horse_name,
                       r.raceName,
                       tr.trackName,
                       r.raceDate,
                       rr.prize
                FROM Trainer t
                JOIN Horse h ON h.stableId = t.stableId
                JOIN RaceResults rr ON h.horseId = rr.horseId AND rr.results = 'first'
                JOIN Race r ON rr.raceId = r.raceId
                JOIN Track tr ON r.trackName = tr.trackName
                ORDER BY r.raceDate DESC
            """
            
            results = self.db_manager.execute_query(query)
            
            if results:
                for row in results:
                    self.winners_tree.insert("", tk.END, values=(
                        row['trainer_name'],
                        row['horse_name'],
                        row['raceName'],
                        row['trackName'],
                        row['raceDate'],
                        f"${row['prize']:,.2f}" if row['prize'] else "$0.00"
                    ))
            else:
                messagebox.showinfo("No Results", "No trainers found with first place wins")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search winning trainers: {e}")
    
    def search_trainer_winnings(self):
        """Search trainers sorted by total winnings"""
        try:
            # Clear existing results
            for item in self.winnings_tree.get_children():
                self.winnings_tree.delete(item)
            
            query = """
                SELECT CONCAT(t.fname, ' ', t.lname) as trainer_name,
                       IFNULL(SUM(rr.prize), 0) as total_winnings,
                       COUNT(CASE WHEN rr.results = 'first' THEN 1 END) as num_wins,
                       s.stableName
                FROM Trainer t
                LEFT JOIN Horse h ON h.stableId = t.stableId
                LEFT JOIN RaceResults rr ON h.horseId = rr.horseId
                LEFT JOIN Stable s ON t.stableId = s.stableId
                GROUP BY t.trainerId, t.fname, t.lname, s.stableName
                ORDER BY total_winnings DESC
            """
            
            results = self.db_manager.execute_query(query)
            
            if results:
                for row in results:
                    self.winnings_tree.insert("", tk.END, values=(
                        row['trainer_name'],
                        f"${row['total_winnings']:,.2f}",
                        row['num_wins'],
                        row['stableName']
                    ))
            else:
                messagebox.showinfo("No Results", "No trainers found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search trainer winnings: {e}")
    
    def search_track_stats(self):
        """Search track statistics"""
        try:
            # Clear existing results
            for item in self.tracks_tree.get_children():
                self.tracks_tree.delete(item)
            
            query = """
                SELECT tr.trackName,
                       tr.location,
                       tr.length,
                       COUNT(DISTINCT r.raceId) as num_races,
                       COUNT(DISTINCT rr.horseId) as total_horses
                FROM Track tr
                LEFT JOIN Race r ON tr.trackName = r.trackName
                LEFT JOIN RaceResults rr ON r.raceId = rr.raceId
                GROUP BY tr.trackName, tr.location, tr.length
                ORDER BY tr.trackName
            """
            
            results = self.db_manager.execute_query(query)
            
            if results:
                for row in results:
                    self.tracks_tree.insert("", tk.END, values=(
                        row['trackName'],
                        row['location'],
                        f"{row['length']} miles" if row['length'] else "N/A",
                        row['num_races'],
                        row['total_horses']
                    ))
            else:
                messagebox.showinfo("No Results", "No tracks found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search track statistics: {e}")
    
    def back_to_main(self):
        """Return to main menu"""
        self.root.destroy()
        self.back_callback()