import customtkinter as ctk
from datetime import datetime, date
import calendar
from typing import Optional, Dict
import sys
import os
# Add the current directory to the path so we can import from database
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.checker import Database

class DiaryApp:
    def __init__(self):
        # Initialize database
        self.db = Database()
        self.setup_database()
        
        # Initialize GUI
        self.root = ctk.CTk()
        self.root.title("Diary Application")
        self.root.geometry("1200x800")
        
        # Current selected date
        self.selected_date: Optional[date] = None
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        # Available years range
        self.year_range = (1998, 2025)
        
        # Cache for entries
        self.entries_cache: Dict[str, str] = {}
        
        self.setup_ui()
        self.load_entries()
        
    def setup_database(self):
        """Create the diary entries table if it doesn't exist"""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS diary_entries (
                date TEXT PRIMARY KEY,
                content TEXT
            )
        """)
        
    def setup_ui(self):
        """Setup the main UI with two panels"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Calendar overview
        self.left_panel = ctk.CTkFrame(self.main_frame)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Right panel - Entry editor
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.setup_left_panel()
        self.setup_right_panel()
        
    def setup_left_panel(self):
        """Setup the calendar overview panel"""
        # Create horizontal layout for month selection and calendar
        content_frame = ctk.CTkFrame(self.left_panel)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Month selection on the left (vertical buttons) - compact
        self.month_frame = ctk.CTkFrame(content_frame)
        self.month_frame.pack(side="left", fill="y", padx=(0, 3))
        
        # Create a scrollable frame for month buttons - very compact
        self.month_scroll = ctk.CTkScrollableFrame(self.month_frame, width=80)
        self.month_scroll.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Create month buttons vertically - compact
        self.month_buttons = {}
        month_names = [
            "Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
            "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"
        ]
        
        for i, month_name in enumerate(month_names, 1):
            btn = ctk.CTkButton(
                self.month_scroll,
                text=month_name,
                command=lambda m=i: self.on_month_changed(m),
                height=25,
                width=70,
                font=("Arial", 9)
            )
            btn.pack(fill="x", padx=2, pady=1)
            self.month_buttons[i] = btn
        
        # Calendar area with year-day grid on the right
        self.calendar_frame = ctk.CTkFrame(content_frame)
        self.calendar_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Set current month as active and highlight it
        self.current_month_button = self.month_buttons[self.current_month]
        self.current_month_button.configure(fg_color=("blue", "darkblue"))
        
        # Create initial calendar for current month
        self.create_month_calendar(None, self.current_month)
        
    def create_month_calendar(self, parent, month_num):
        """Create calendar grid for a specific month with years as rows and days as columns"""
        # Clear existing calendar content
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for the year-day grid - compact
        scroll_frame = ctk.CTkScrollableFrame(self.calendar_frame)
        scroll_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Get number of days in the month (using current year as reference)
        num_days = calendar.monthrange(self.current_year, month_num)[1]
        
        # Create header row with day numbers - compact
        header_frame = ctk.CTkFrame(scroll_frame)
        header_frame.pack(fill="x", pady=(0, 2))
        
        # Year column header - compact
        ctk.CTkLabel(header_frame, text="Jahr", font=("Arial", 9, "bold"), width=40).pack(side="left", padx=1)
        
        # Day headers - compact
        for day in range(1, num_days + 1):
            day_label = ctk.CTkLabel(header_frame, text=str(day), font=("Arial", 8, "bold"), width=18)
            day_label.pack(side="left", padx=0)
        
        # Create rows for each year - compact
        self.day_buttons = {}
        for year in range(self.year_range[0], self.year_range[1] + 1):
            year_frame = ctk.CTkFrame(scroll_frame)
            year_frame.pack(fill="x", pady=0)
            
            # Year label - compact
            year_label = ctk.CTkLabel(year_frame, text=str(year), font=("Arial", 9, "bold"), width=40)
            year_label.pack(side="left", padx=1)
            
            # Day buttons for this year - compact
            for day in range(1, num_days + 1):
                # Create closure to capture the current values
                def make_click_handler(d, m, y):
                    return lambda: self.on_day_clicked(d, m, y)
                
                btn = ctk.CTkButton(
                    year_frame,
                    text="",
                    width=18,
                    height=18,
                    command=make_click_handler(day, month_num, year),
                    font=("Arial", 7)
                )
                btn.pack(side="left", padx=0)
                
                # Store button reference
                date_key = f"{year}-{month_num:02d}-{day:02d}"
                self.day_buttons[date_key] = btn
                
                # Check if there's content for this date
                if date_key in self.entries_cache:
                    btn.configure(fg_color=("green", "darkgreen"))
                else:
                    btn.configure(fg_color=("gray75", "gray25"))
                        
    def setup_right_panel(self):
        """Setup the entry editor panel"""
        # Header with date
        self.date_header = ctk.CTkLabel(
            self.right_panel, 
            text="Wählen Sie ein Datum zum Anzeigen/Bearbeiten",
            font=("Arial", 16, "bold")
        )
        self.date_header.pack(pady=20)
        
        # Text editor
        self.text_editor = ctk.CTkTextbox(
            self.right_panel,
            font=("Arial", 12),
            wrap="word"
        )
        self.text_editor.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Save button
        self.save_button = ctk.CTkButton(
            self.right_panel,
            text="Eintrag speichern",
            command=self.save_entry,
            font=("Arial", 14, "bold"),
            height=40
        )
        self.save_button.pack(pady=20)
        
    def on_month_changed(self, month_num):
        """Handle month change"""
        # Reset previous button color
        if hasattr(self, 'current_month_button'):
            self.current_month_button.configure(fg_color=("gray75", "gray25"))
        
        # Highlight new button
        self.current_month_button = self.month_buttons[month_num]
        self.current_month_button.configure(fg_color=("blue", "darkblue"))
        
        # Update current month
        self.current_month = month_num
        
        # Refresh calendar
        self.refresh_calendar()
        
    def on_day_clicked(self, day, month, year):
        """Handle day button click"""
        self.selected_date = date(year, month, day)
        self.update_date_header()
        self.load_entry_content()
        
    def update_date_header(self):
        """Update the date header with the selected date"""
        if self.selected_date:
            # Format date in German
            weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            weekday = weekdays[self.selected_date.weekday()]
            formatted_date = f"{weekday}, {self.selected_date.day:02d}.{self.selected_date.month:02d}.{self.selected_date.year}"
            self.date_header.configure(text=formatted_date)
            
    def load_entry_content(self):
        """Load content for the selected date"""
        if self.selected_date:
            date_key = self.selected_date.strftime("%Y-%m-%d")
            content = self.entries_cache.get(date_key, "")
            self.text_editor.delete("1.0", "end")
            self.text_editor.insert("1.0", content)
            
    def save_entry(self):
        """Save the current entry to database"""
        if self.selected_date:
            date_key = self.selected_date.strftime("%Y-%m-%d")
            content = self.text_editor.get("1.0", "end-1c")
            
            # Save to database
            self.db.execute(
                "INSERT OR REPLACE INTO diary_entries (date, content) VALUES (?, ?)",
                (date_key, content)
            )
            
            # Update cache
            self.entries_cache[date_key] = content
            
            # Update button color
            if date_key in self.day_buttons:
                if content.strip():
                    self.day_buttons[date_key].configure(fg_color=("green", "darkgreen"))
                else:
                    self.day_buttons[date_key].configure(fg_color=("gray75", "gray25"))
                    
            print(f"Entry saved for {date_key}")
            
    def load_entries(self):
        """Load all entries from database into cache"""
        entries = self.db.query("SELECT date, content FROM diary_entries")
        self.entries_cache = {entry["date"]: entry["content"] for entry in entries}
        
    def refresh_calendar(self):
        """Refresh the calendar display"""
        # Refresh the calendar for the current month
        self.create_month_calendar(None, self.current_month)
            
    def run(self):
        """Start the application"""
        self.root.mainloop()
        self.db.close()

if __name__ == "__main__":
    app = DiaryApp()
    app.run()
