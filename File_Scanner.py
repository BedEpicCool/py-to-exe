import os
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import subprocess
import platform

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
    system_exes = {"explorer.exe", "notepad.exe", "wordpad.exe", "calc.exe", "mspaint.exe", "solitaire.exe", "minesweeper.exe"}
    
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
root.title("Windows App Launcher")

# Get the list of .exe files
exe_files = scan_for_exes(C_DRIVE)

# If no .exe files found, show a message and exit
if not exe_files:
    messagebox.showinfo("No Apps", "No .exe files found in C drive.")
    root.quit()

# Map exe names to full paths
exe_name_to_path = {os.path.basename(exe): exe for exe in exe_files}

# Create a listbox to display the .exe files
listbox = tk.Listbox(root, height=15, width=50)
for exe_name in sorted(exe_name_to_path.keys()):
    listbox.insert(tk.END, exe_name)

# Function to handle app selection
def on_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_name = listbox.get(selected_index)
        selected_exe = exe_name_to_path[selected_name]
        launch_app(selected_exe)

# Bind the selection event
listbox.bind("<Double-1>", on_select)

# Add the listbox to the window
listbox.pack(padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()