import os
import tkinter as tk
from tkinter import messagebox, font
import subprocess
import platform

# Custom rounded entry widget using Canvas
class RoundedEntry(tk.Frame):
    def __init__(self, parent, width=300, height=40, bg_color="#1a1f3a", text_color="#ffffff", 
                 corner_radius=10, **kwargs):
        super().__init__(parent, bg=parent["bg"])
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg=parent["bg"], 
                               highlightthickness=0, relief=tk.FLAT, bd=0)
        self.canvas.pack()
        
        # Draw rounded rectangle with arcs and lines
        self._draw_rounded_rectangle(self.canvas, 0, 0, width, height, corner_radius, bg_color)
        
        # Create entry widget
        self.entry = tk.Entry(self.canvas, font=("Arial", 11), bg=bg_color, fg=text_color,
                             insertbackground="#4285f4", relief=tk.FLAT, bd=0, **kwargs)
        self.canvas.create_window(width//2, height//2, window=self.entry, width=width-20)
    
    def _draw_rounded_rectangle(self, canvas, x, y, width, height, radius, fill_color):
        # Draw corners with arcs
        canvas.create_arc(x, y, x+radius*2, y+radius*2, start=90, extent=90, fill=fill_color, outline=fill_color)
        canvas.create_arc(x+width-radius*2, y+radius*2, x+width, y, start=0, extent=90, fill=fill_color, outline=fill_color)
        canvas.create_arc(x+width-radius*2, y+height-radius*2, x+width, y+height, start=270, extent=90, fill=fill_color, outline=fill_color)
        canvas.create_arc(x+radius*2, y+height-radius*2, x+radius*2, y+height, start=180, extent=90, fill=fill_color, outline=fill_color)
        
        # Draw connecting lines
        canvas.create_rectangle(x+radius, y, x+width-radius, y+height, fill=fill_color, outline=fill_color)
        canvas.create_rectangle(x, y+radius, x+width, y+height-radius, fill=fill_color, outline=fill_color)
        
        # Draw border with arcs
        canvas.create_arc(x, y, x+radius*2, y+radius*2, start=90, extent=90, outline="#4285f4", width=2)
        canvas.create_arc(x+width-radius*2, y+radius*2, x+width, y, start=0, extent=90, outline="#4285f4", width=2)
        canvas.create_arc(x+width-radius*2, y+height-radius*2, x+width, y+height, start=270, extent=90, outline="#4285f4", width=2)
        canvas.create_arc(x+radius*2, y+height-radius*2, x+radius*2, y+height, start=180, extent=90, outline="#4285f4", width=2)
        
        # Draw border lines
        canvas.create_line(x+radius, y, x+width-radius, y, fill="#4285f4", width=2)
        canvas.create_line(x+radius, y+height, x+width-radius, y+height, fill="#4285f4", width=2)
        canvas.create_line(x, y+radius, x, y+height-radius, fill="#4285f4", width=2)
        canvas.create_line(x+width, y+radius, x+width, y+height-radius, fill="#4285f4", width=2)
    
    def get(self):
        return self.entry.get()
    
    def delete(self, *args):
        return self.entry.delete(*args)
    
    def insert(self, *args):
        return self.entry.insert(*args)

# Custom rounded button widget using Canvas
class RoundedButton(tk.Frame):
    def __init__(self, parent, text="", command=None, width=200, height=50, 
                 bg_color="#4285f4", text_color="#ffffff", corner_radius=10, **kwargs):
        super().__init__(parent, bg=parent["bg"])
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg=parent["bg"], 
                               highlightthickness=0, relief=tk.FLAT, bd=0, cursor="hand2")
        self.canvas.pack()
        
        # Draw rounded rectangle
        self._draw_rounded_rectangle(self.canvas, 0, 0, width, height, corner_radius, bg_color)
        
        # Create button widget
        self.button = tk.Button(self.canvas, text=text, command=command, 
                               font=("Arial", 12, "bold"), bg=bg_color, fg=text_color,
                               relief=tk.FLAT, bd=0, activebackground=bg_color, 
                               activeforeground=text_color, **kwargs)
        self.canvas.create_window(width//2, height//2, window=self.button, width=width-20)
    
    def _draw_rounded_rectangle(self, canvas, x, y, width, height, radius, fill_color):
        # Draw corners with arcs
        canvas.create_arc(x, y, x+radius*2, y+radius*2, start=90, extent=90, fill=fill_color, outline=fill_color)
        canvas.create_arc(x+width-radius*2, y+radius*2, x+width, y, start=0, extent=90, fill=fill_color, outline=fill_color)
        canvas.create_arc(x+width-radius*2, y+height-radius*2, x+width, y+height, start=270, extent=90, fill=fill_color, outline=fill_color)
        canvas.create_arc(x+radius*2, y+height-radius*2, x+radius*2, y+height, start=180, extent=90, fill=fill_color, outline=fill_color)
        
        # Draw connecting rectangles
        canvas.create_rectangle(x+radius, y, x+width-radius, y+height, fill=fill_color, outline=fill_color)
        canvas.create_rectangle(x, y+radius, x+width, y+height-radius, fill=fill_color, outline=fill_color)

# Custom rounded listbox widget using Canvas
class RoundedListbox(tk.Frame):
    def __init__(self, parent, width=500, height=400, bg_color="#1a1f3a", 
                 text_color="#ffffff", corner_radius=10, **kwargs):
        super().__init__(parent, bg=parent["bg"])
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg=parent["bg"], 
                               highlightthickness=0, relief=tk.FLAT, bd=0)
        self.canvas.pack()
        
        # Draw rounded rectangle background
        self._draw_rounded_rectangle(self.canvas, 0, 0, width, height, corner_radius, bg_color)
        
        # Create listbox widget with padding
        padding = 8
        self.listbox = tk.Listbox(self.canvas, font=("Arial", 12), 
                                 bg=bg_color, fg=text_color, selectbackground="#4285f4", 
                                 selectforeground=text_color, borderwidth=0, 
                                 highlightthickness=0, activestyle='dotbox', **kwargs)
        self.canvas.create_window(width//2, height//2, window=self.listbox, 
                                 width=width-padding*2, height=height-padding*2)
    
    def _draw_rounded_rectangle(self, canvas, x, y, width, height, radius, fill_color):
        # Draw corners with arcs
        canvas.create_arc(x, y, x+radius*2, y+radius*2, start=90, extent=90, fill=fill_color, outline="#4285f4", width=2)
        canvas.create_arc(x+width-radius*2, y+radius*2, x+width, y, start=0, extent=90, fill=fill_color, outline="#4285f4", width=2)
        canvas.create_arc(x+width-radius*2, y+height-radius*2, x+width, y+height, start=270, extent=90, fill=fill_color, outline="#4285f4", width=2)
        canvas.create_arc(x+radius*2, y+height-radius*2, x+radius*2, y+height, start=180, extent=90, fill=fill_color, outline="#4285f4", width=2)
        
        # Draw connecting rectangles
        canvas.create_rectangle(x+radius, y, x+width-radius, y+height, fill=fill_color, outline=fill_color)
        canvas.create_rectangle(x, y+radius, x+width, y+height-radius, fill=fill_color, outline=fill_color)
        
        # Draw border lines
        canvas.create_line(x+radius, y, x+width-radius, y, fill="#4285f4", width=2)
        canvas.create_line(x+radius, y+height, x+width-radius, y+height, fill="#4285f4", width=2)
        canvas.create_line(x, y+radius, x, y+height-radius, fill="#4285f4", width=2)
        canvas.create_line(x+width, y+radius, x+width, y+height-radius, fill="#4285f4", width=2)
    
    def curselection(self):
        return self.listbox.curselection()
    
    def get(self, index):
        return self.listbox.get(index)
    
    def insert(self, index, *items):
        return self.listbox.insert(index, *items)
    
    def delete(self, first, last=None):
        return self.listbox.delete(first, last)
    
    def bind(self, sequence, func, add=None):
        return self.listbox.bind(sequence, func, add)

# Define the directory to search for .exe files (entire C drive)
if platform.system() == "Windows":
    # When running on Windows, use the actual C: drive
    C_DRIVE = "C:\\"
else:
    # When running on macOS, use the Sikarugir path
    C_DRIVE = os.path.expanduser("~/Applications/Sikarugir/MasterWrapper.app/Contents/SharedSupport/prefix/drive_c")

# Function to scan for .exe files
def scan_for_exes(directory):
    exes = []
    # System directories to exclude
    system_dirs = {"system32", "syswow64", "windows", "drivers", "wbem", "tasks", "prefetch", "$recycle.bin"}
    # Windows built-in applications to exclude
    system_exes = {"explorer.exe", "notepad.exe", "wordpad.exe", "calc.exe", "mspaint.exe", "solitaire.exe", "minesweeper.exe", "file_scanner.exe", "iexplore.exe", "wmplayer.exe"}
    
    for root, dirs, files in os.walk(directory):
        # Remove system directories from dirs to skip traversing them
        dirs[:] = [d for d in dirs if d.lower() not in system_dirs]
        
        for file in files:
            if file.endswith(".exe") and file.lower() not in system_exes:
                exes.append(os.path.join(root, file))
    return exes

# Function to launch selected .exe file
def launch_app(exe_path):
    try:
        # Launch from the app's directory so it can find its resources/DLLs
        app_dir = os.path.dirname(exe_path)
        subprocess.Popen([exe_path], cwd=app_dir, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch {exe_path}:\n{str(e)}")

# Create the main window
root = tk.Tk()
root.title("App Launcher")
root.geometry("700x800")
root.configure(bg="#0a0e27")

# Define blue-purple gradient colors
PRIMARY_COLOR = "#4285f4"  # Blue
SECONDARY_COLOR = "#7c3aed"  # Purple
ACCENT_COLOR = "#a78bfa"  # Light purple
BG_COLOR = "#0a0e27"  # Dark blue-black
CARD_BG = "#1a1f3a"  # Darker blue
TEXT_COLOR = "#ffffff"
HOVER_COLOR = "#5a96ff"

# Get the list of .exe files
exe_files = scan_for_exes(C_DRIVE)

# If no .exe files found, show a message and exit
if not exe_files:
    messagebox.showinfo("No Apps", "No .exe files found in C drive.")
    root.quit()

# Map exe names to full paths
exe_name_to_path = {os.path.basename(exe): exe for exe in exe_files}
sorted_apps = sorted(exe_name_to_path.keys())

# Title label with gradient effect
title_font = font.Font(family="Arial", size=22, weight="bold")
title_label = tk.Label(root, text="🚀 App Launcher", font=title_font, bg=BG_COLOR, fg=PRIMARY_COLOR)
title_label.pack(pady=30)

subtitle_font = font.Font(family="Arial", size=10)
subtitle_label = tk.Label(root, text="Double-click to launch or use the Launch button", font=subtitle_font, bg=BG_COLOR, fg=ACCENT_COLOR)
subtitle_label.pack(pady=(0, 20))

# Search frame with rounded style
search_frame = tk.Frame(root, bg=BG_COLOR)
search_frame.pack(padx=25, pady=(0, 15), fill=tk.X)

search_label = tk.Label(search_frame, text="🔍 Search:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 11, "bold"))
search_label.pack(side=tk.LEFT, padx=(0, 10))

search_var = tk.StringVar()
search_entry_frame = RoundedEntry(search_frame, width=400, height=40, bg_color=CARD_BG, 
                                  text_color=TEXT_COLOR, corner_radius=12, textvariable=search_var)
search_entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Listbox with scrollbar in a nice container
list_frame = tk.Frame(root, bg=BG_COLOR)
list_frame.pack(padx=25, pady=(0, 20), fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(list_frame, bg=CARD_BG, troughcolor=BG_COLOR, activebackground=PRIMARY_COLOR)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = RoundedListbox(list_frame, width=600, height=350, bg_color=CARD_BG, 
                        text_color=TEXT_COLOR, corner_radius=15, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.listbox.yview)

for app_name in sorted_apps:
    listbox.insert(tk.END, app_name)

# Filter function
def filter_apps(*args):
    search_text = search_var.get().lower()
    listbox.delete(0, tk.END)
    
    for app_name in sorted_apps:
        if search_text == "" or search_text in app_name.lower():
            listbox.insert(tk.END, app_name)

search_var.trace_add("write", filter_apps)

# Function to handle app selection
def on_select(event=None):
    selected_index = listbox.curselection()
    if selected_index:
        selected_name = listbox.get(selected_index)
        if selected_name in exe_name_to_path:
            selected_exe = exe_name_to_path[selected_name]
            launch_app(selected_exe)

# Bind the selection event
listbox.bind("<Double-1>", on_select)

# Button frame with better styling
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(padx=25, pady=(0, 25), fill=tk.X)

launch_button = RoundedButton(button_frame, text="▶  Launch App", command=on_select, 
                              width=280, height=50, bg_color=PRIMARY_COLOR, 
                              text_color=TEXT_COLOR, corner_radius=12)
launch_button.pack(side=tk.LEFT, padx=(0, 12), fill=tk.X, expand=True)

refresh_button = RoundedButton(button_frame, text="🔄  Refresh",
                               width=280, height=50, bg_color=SECONDARY_COLOR, 
                               text_color=TEXT_COLOR, corner_radius=12)
refresh_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Start the Tkinter event loop
root.mainloop()
root.mainloop()