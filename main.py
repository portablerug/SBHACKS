import tkinter as tk  # Import tkinter for GUI
from tkinter import messagebox  # Import messagebox for showing alerts
import psutil  # Import psutil for system and process utilities
from plyer import notification  # Import notification module from plyer for desktop notifications
import threading  # Import threading for concurrent execution
import browserhistory as bh  # Import browserhistory for fetching browser history
import sqlite3  # Import sqlite3 for database operations
import time  # Import time for time-related functions
import os  # Import os for file path operations
import pandas as pd  # Import pandas for data manipulation
import matplotlib.pyplot as plt  # Import matplotlib for plotting graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import FigureCanvasTkAgg for embedding matplotlib figures in Tkinter
from urllib.parse import urlparse  # Import urlparse for URL parsing

bg_color = '#2e2e2e'
fg_color = '#ffffff'
button_bg_color = '#4CAF50'
button_fg_color = '#36454F'
highlight_bg_color = '#444444''

#testing
# Get the directory of the executable or script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the database file
DB_PATH = os.path.join(BASE_DIR, 'chrome_history.db')

def setup_database():
    conn = sqlite3.connect(DB_PATH)  # Connect to (or create) the SQLite database
    cursor = conn.cursor()  # Create a cursor object for executing SQL commands
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      url TEXT,
                      title TEXT,
                      date TEXT)''')  # Create the 'history' table if it doesn't exist
    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

def is_chrome_running():
    for process in psutil.process_iter(['pid', 'name']):  # Iterate over all running processes
        if 'chrome' in process.info['name'].lower():  # Check if the process name contains 'chrome'
            return True  # Return True if Chrome is running
    return False  # Return False if Chrome is not running

def fetch_browser_history(last_fetch):
    history = bh.get_browserhistory()  # Fetch the browser history using the browserhistory library
    chrome_history = history.get("chrome", [])  # Extract Chrome history from the fetched history
    new_entries = [entry for entry in chrome_history if entry[2] > last_fetch]  # Filter new entries since the last fetch
    return new_entries, chrome_history[-1][2] if chrome_history else last_fetch  # Return new entries and the latest fetch time

def store_history_to_db(entries):
    conn = sqlite3.connect(DB_PATH)  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object
    for entry in entries:
        cursor.execute('INSERT INTO history (url, title, date) VALUES (?, ?, ?)', (entry[0], entry[1], entry[2]))  # Insert each entry into the 'history' table
    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

def monitor_chrome():
    chrome_open = False  # Initialize a flag to check if Chrome is open
    last_fetch = '2024-01-01 00:00:00'  # Initialize the last fetch time
    
    while True:
        chrome_currently_running = is_chrome_running()  # Check if Chrome is running
        
        if chrome_currently_running and not chrome_open:
            notification.notify(
                title='Google Chrome Notification',
                message='Google Chrome has been opened.',
                timeout=10
            )  # Display a notification when Chrome is opened
            chrome_open = True  # Set the flag to True
        
        if chrome_open:
            new_entries, last_fetch = fetch_browser_history(last_fetch)  # Fetch new browser history
            if new_entries:
                store_history_to_db(new_entries)  # Store new entries in the database
                update_ui.set()  # Set the flag to update UI
        
        if not chrome_currently_running and chrome_open:
            notification.notify(
                title='Google Chrome Notification',
                message='Google Chrome has been closed.',
                timeout=10
            )  # Display a notification when Chrome is closed
            chrome_open = False  # Set the flag to False
        
        time.sleep(60)  # Add a sleep duration to control the monitoring frequency

def read_data_from_db():
    conn = sqlite3.connect(DB_PATH)  # Connect to the SQLite database
    query = "SELECT url, title, date FROM history"  # Define the SQL query to fetch data from the 'history' table
    df = pd.read_sql(query, conn)  # Read the data into a pandas DataFrame
    conn.close()  # Close the database connection

    # Extract domains from URLs
    df['domain'] = df['url'].apply(lambda url: urlparse(url).netloc)
    
    # Group by domain and count occurrences
    domain_counts = df['domain'].value_counts().reset_index()
    domain_counts.columns = ['domain', 'count']
    
    return domain_counts  # Return the cleaned and sorted DataFrame

def show_automations():
    domain_counts = read_data_from_db()
    if domain_counts.empty:
        info_label.configure(text="No data found in the database.")
    else:
        history_text = domain_counts.to_string(index=False)
        info_label.configure(text=history_text)

        # Create a bar graph of the top domains
        top_domains = domain_counts.head(5)
        fig, ax = plt.subplots()
        top_domains.plot(kind='bar', x='domain', y='count', ax=ax)
        ax.set_title('Top Google Chrome Domains')
        ax.set_xlabel('Domain')
        ax.set_ylabel('Frequency')
        
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

def switch_to_automations():
    main_frame.pack_forget()
    automations_frame.pack(fill="both", expand=True)
    update_automations_display()

def switch_to_main():
    automations_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def update_automations_display():
    if update_ui.is_set():
        show_automations()
        update_ui.clear()
    root.after(5000, update_automations_display)  # Refresh every 5 seconds

def submit():
    if chrome_var.get() == "Google Chrome":
        threading.Thread(target=monitor_chrome, daemon=True).start()  # Start monitoring Chrome in the background

# Main application window
root = tk.Tk()
root.title("Automation App")
root.geometry("800x600")

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Create a label for the main tab
app_label = tk.Label(main_frame, text="Automation App", font=("Arial", 24))
app_label.pack(pady=20)

# Create checkboxes
vs_code_var = tk.StringVar()
chrome_var = tk.StringVar()
gmail_var = tk.StringVar()

vs_code_checkbox = tk.Checkbutton(main_frame, text="VS Code", variable=vs_code_var, onvalue="VS Code", offvalue="")
chrome_checkbox = tk.Checkbutton(main_frame, text="Google Chrome", variable=chrome_var, onvalue="Google Chrome", offvalue="")
gmail_checkbox = tk.Checkbutton(main_frame, text="Gmail", variable=gmail_var, onvalue="Gmail", offvalue="")

vs_code_checkbox.pack(pady=10)
chrome_checkbox.pack(pady=10)
gmail_checkbox.pack(pady=10)

# Create a submit button
submit_button = tk.Button(main_frame, text="Submit", command=submit, bg=button_bg_color, fg=button_fg_color)
submit_button.pack(pady=10)

# Create a button to switch to automations
automations_button = tk.Button(main_frame, text="View Automations", command=switch_to_automations, bg = button_bg_color,  fg = button_fg_color)
automations_button.pack(pady=10)

# Create automations frame
automations_frame = tk.Frame(root)

# Create a back button to switch to the main frame
back_button = tk.Button(automations_frame, text="Back", command=switch_to_main, bg = button_bg_color, fg=button_fg_color)
back_button.pack(pady=10)

# Automations tab widgets
history_frame = tk.Frame(automations_frame)
history_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

graph_frame = tk.Frame(automations_frame)
graph_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

info_label = tk.Label(history_frame, text="Database Information", font=("Arial", 14), justify="left", bg = bg_color, fg=fg_color)
info_label.pack(pady=20, padx=20)

# Setup the database
setup_database()

# Refresh the automations display regularly
update_ui = threading.Event()
root.after(5000, update_automations_display)  # Refresh every 5 seconds

# Run the Tkinter main loop
root.mainloop()
