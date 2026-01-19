import time
import tkinter as tk
from tkinter import messagebox, filedialog
from openpyxl import Workbook
from pynput import keyboard
import threading

# Define behaviors and associated keys
events = {
    'y': {'name': 'Sniffing', 'frequency': 0, 'duration': 0.0, 'start_time': None},
    'x': {'name': 'Following', 'frequency': 0, 'duration': 0.0, 'start_time': None},
    'm': {'name': 'Mounting', 'frequency': 0, 'duration': 0.0, 'start_time': None},
    'n': {'name': 'Push & Crawl', 'frequency': 0, 'duration': 0.0, 'start_time': None},
    'o': {'name': 'Allogrooming', 'frequency': 0, 'duration': 0.0, 'start_time': None},
    'p': {'name': 'Affiliative', 'frequency': 0, 'duration': 0.0, 'start_time': None},
}

key_states = {key: False for key in events}

def on_button_press(key):
    if not key_states[key]:
        key_states[key] = True
        events[key]['start_time'] = time.time()

def on_button_release(key):
    if key_states[key]:
        key_states[key] = False
        held_time = time.time() - events[key]['start_time']
        events[key]['duration'] += held_time
        events[key]['frequency'] += 1
        events[key]['start_time'] = None
        update_labels()

def update_labels():
    for key in events:
        if key_states[key] and events[key]['start_time'] is not None:
            current_duration = events[key]['duration'] + (time.time() - events[key]['start_time'])
        else:
            current_duration = events[key]['duration']
        freq_labels[key].config(text=f"Freq: {events[key]['frequency']}")
        dur_labels[key].config(text=f"Dur: {current_duration:.1f}s")

def save_results():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx")],
                                             title="Save Results As")
    if file_path:
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Behavior Results"
            ws.append(['Event', 'Frequency', 'Total Duration (s)'])
            for k in events:
                ws.append([
                    events[k]['name'],
                    events[k]['frequency'],
                    round(events[k]['duration'], 3)
                ])
            wb.save(file_path)
            messagebox.showinfo("Saved", f"Results saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

def reset_counters():
    for k in events:
        events[k]['frequency'] = 0
        events[k]['duration'] = 0.0
        events[k]['start_time'] = None
        key_states[k] = False
    update_labels()

def update_live_durations():
    update_labels()
    root.after(100, update_live_durations)  # Update every 100ms

# Keyboard listener using pynput
def on_press(key):
    try:
        k = key.char.lower()
        if k in events:
            on_button_press(k)
    except AttributeError:
        pass

def on_release(key):
    try:
        k = key.char.lower()
        if k in events:
            on_button_release(k)
    except AttributeError:
        pass

def start_keyboard_listener():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.daemon = True
    listener.start()

# GUI Setup
root = tk.Tk()
root.title("Social Behavior Counter")
root.geometry("370x300")

main_frame = tk.Frame(root)
main_frame.pack(pady=10)

freq_labels = {}
dur_labels = {}

row = 0
col = 0
for key in events:
    frame = tk.Frame(main_frame, relief=tk.RAISED, bd=1, padx=5, pady=5)
    frame.grid(row=row, column=col, padx=5, pady=5, sticky="n")

    btn = tk.Button(frame, text=events[key]['name'], width=16, height=1)
    btn.pack()
    btn.bind("<ButtonPress-1>", lambda e, k=key: on_button_press(k))
    btn.bind("<ButtonRelease-1>", lambda e, k=key: on_button_release(k))

    freq_label = tk.Label(frame, text="Freq: 0", font=("Arial", 9))
    freq_label.pack()
    freq_labels[key] = freq_label

    dur_label = tk.Label(frame, text="Dur: 0.0s", font=("Arial", 9))
    dur_label.pack()
    dur_labels[key] = dur_label

    col += 1
    if col == 3:
        col = 0
        row += 1

# Save and reset buttons
controls = tk.Frame(root)
controls.pack(pady=5)

tk.Button(controls, text="Save Results", command=save_results, bg="lightgreen", width=15).grid(row=0, column=0, padx=10)
tk.Button(controls, text="Reset", command=reset_counters, bg="tomato", width=10).grid(row=0, column=1)

# Start everything
start_keyboard_listener()
update_live_durations()
root.mainloop()
