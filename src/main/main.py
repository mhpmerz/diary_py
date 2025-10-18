"""The main module for starting the application"""

import customtkinter as ctk
from database.checker import db
import sqlite3
from datetime import datetime, date
import os

class DiaryApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Diary PY")
        self.root.geometry("800x600")
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_widgets()
        
    def init_database(self):
        """Initialize the database with diary entries table"""
        try:
            # Create diary entries table if it doesn't exist
            db.execute("""
                CREATE TABLE IF NOT EXISTS diary_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    title TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Diary PY", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)
        
        # Search frame
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Search entry
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Search diary entries...",
            textvariable=self.search_var,
            width=400
        )
        self.search_entry.pack(side="left", padx=5, pady=5)
        
        # Search button
        search_button = ctk.CTkButton(
            search_frame, 
            text="Search",
            command=self.search_entries,
            width=100
        )
        search_button.pack(side="left", padx=5, pady=5)
        
        # Clear search button
        clear_button = ctk.CTkButton(
            search_frame, 
            text="Clear",
            command=self.clear_search,
            width=100
        )
        clear_button.pack(side="left", padx=5, pady=5)
        
        # Results frame
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Results label
        self.results_label = ctk.CTkLabel(results_frame, text="Search Results:", font=("Arial", 16, "bold"))
        self.results_label.pack(anchor="w", padx=10, pady=5)
        
        # Results text area
        self.results_text = ctk.CTkTextbox(results_frame, height=300)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add entry frame
        add_frame = ctk.CTkFrame(main_frame)
        add_frame.pack(fill="x", padx=10, pady=5)
        
        # Add entry button
        add_button = ctk.CTkButton(
            add_frame, 
            text="Add New Entry",
            command=self.add_entry,
            width=150
        )
        add_button.pack(side="left", padx=5, pady=5)
        
        # Load sample data button
        sample_button = ctk.CTkButton(
            add_frame, 
            text="Load Sample Data",
            command=self.load_sample_data,
            width=150
        )
        sample_button.pack(side="left", padx=5, pady=5)
        
        # Bind Enter key to search
        self.search_entry.bind("<Return>", lambda e: self.search_entries())
        
        # Load all entries on startup
        self.load_all_entries()
    
    def search_entries(self):
        """Search for diary entries based on the search term"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.load_all_entries()
            return
        
        try:
            # Search in title and content
            query = """
                SELECT date, title, content, created_at 
                FROM diary_entries 
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY date DESC
            """
            search_pattern = f"%{search_term}%"
            results = db.query(query, (search_pattern, search_pattern))
            
            self.display_results(results, f"Search results for '{search_term}':")
            
        except Exception as e:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"Search error: {e}")
    
    def clear_search(self):
        """Clear the search and show all entries"""
        self.search_var.set("")
        self.load_all_entries()
    
    def load_all_entries(self):
        """Load all diary entries"""
        try:
            query = "SELECT date, title, content, created_at FROM diary_entries ORDER BY date DESC"
            results = db.query(query)
            self.display_results(results, "All Diary Entries:")
        except Exception as e:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"Error loading entries: {e}")
    
    def display_results(self, results, title):
        """Display search results in the text area"""
        self.results_text.delete("1.0", "end")
        
        if not results:
            self.results_text.insert("1.0", f"{title}\n\nNo entries found.")
            return
        
        self.results_text.insert("1.0", f"{title}\n\n")
        
        for entry in results:
            date_str = entry['date']
            title_str = entry['title'] or "Untitled"
            content_str = entry['content'] or "No content"
            created_at = entry['created_at']
            
            self.results_text.insert("end", f"Date: {date_str}\n")
            self.results_text.insert("end", f"Title: {title_str}\n")
            self.results_text.insert("end", f"Content: {content_str}\n")
            self.results_text.insert("end", f"Created: {created_at}\n")
            self.results_text.insert("end", "-" * 50 + "\n\n")
    
    def add_entry(self):
        """Add a new diary entry"""
        # Create a new window for adding entries
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Add New Entry")
        add_window.geometry("600x400")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Date entry
        date_label = ctk.CTkLabel(add_window, text="Date (YYYY-MM-DD):")
        date_label.pack(pady=5)
        
        date_entry = ctk.CTkEntry(add_window, placeholder_text="2024-01-01")
        date_entry.pack(pady=5)
        date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        
        # Title entry
        title_label = ctk.CTkLabel(add_window, text="Title:")
        title_label.pack(pady=5)
        
        title_entry = ctk.CTkEntry(add_window, placeholder_text="Entry title")
        title_entry.pack(pady=5)
        
        # Content entry
        content_label = ctk.CTkLabel(add_window, text="Content:")
        content_label.pack(pady=5)
        
        content_text = ctk.CTkTextbox(add_window, height=200)
        content_text.pack(pady=5, padx=10, fill="both", expand=True)
        
        def save_entry():
            try:
                entry_date = date_entry.get().strip()
                title = title_entry.get().strip()
                content = content_text.get("1.0", "end").strip()
                
                if not entry_date:
                    return
                
                db.execute(
                    "INSERT INTO diary_entries (date, title, content) VALUES (?, ?, ?)",
                    (entry_date, title, content)
                )
                
                add_window.destroy()
                self.load_all_entries()
                
            except Exception as e:
                print(f"Error saving entry: {e}")
        
        # Save button
        save_button = ctk.CTkButton(add_window, text="Save Entry", command=save_entry)
        save_button.pack(pady=10)
    
    def load_sample_data(self):
        """Load sample diary entries for testing"""
        sample_entries = [
            ("2024-01-15", "First Day", "This is my first diary entry. I'm excited to start this journey!"),
            ("2024-01-16", "Work Day", "Had a productive day at work. Finished the project ahead of schedule."),
            ("2024-01-17", "Weekend Plans", "Planning to visit the museum this weekend. Looking forward to it!"),
            ("2024-01-18", "Learning Python", "Started learning about GUI development with CustomTkinter. It's quite interesting!"),
            ("2024-01-19", "Search Feature", "Implemented a search feature for my diary. Now I can easily find old entries.")
        ]
        
        try:
            for entry_date, title, content in sample_entries:
                db.execute(
                    "INSERT OR IGNORE INTO diary_entries (date, title, content) VALUES (?, ?, ?)",
                    (entry_date, title, content)
                )
            
            self.load_all_entries()
            print("Sample data loaded successfully")
            
        except Exception as e:
            print(f"Error loading sample data: {e}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DiaryApp()
    app.run()
