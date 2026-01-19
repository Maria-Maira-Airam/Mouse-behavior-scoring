import tkinter as tk
from tkinter import messagebox, filedialog
import time
import csv
from datetime import datetime
import os

class BehaviorCounterApp:
    def __init__(self, master):
        self.master = master
        master.title("Behavior Counter")

        self.behaviors = ['Rearing', 'Moving', 'Grooming']
        self.frequency_counts = {b: 0 for b in self.behaviors}
        self.duration_totals = {b: 0.0 for b in self.behaviors}
        self.hold_start_times = {}

        self.freq_labels = {}
        self.dur_labels = {}

        for i, behavior in enumerate(self.behaviors):
            tk.Label(master, text=behavior, font=('Arial', 12, 'bold')).grid(row=i*2, column=0, columnspan=4)

            freq_btn = tk.Button(master, text="Frequency", width=12,
                                 command=lambda b=behavior: self.increment_frequency(b))
            freq_btn.grid(row=i*2+1, column=0)

            dur_btn = tk.Button(master, text="Duration", width=12)
            dur_btn.grid(row=i*2+1, column=1)
            dur_btn.bind('<ButtonPress-1>', lambda event, b=behavior: self.start_hold(b))
            dur_btn.bind('<ButtonRelease-1>', lambda event, b=behavior: self.end_hold(b))

            self.freq_labels[behavior] = tk.Label(master, text="Frequency: 0")
            self.freq_labels[behavior].grid(row=i*2+1, column=2)

            self.dur_labels[behavior] = tk.Label(master, text="0.00 s")
            self.dur_labels[behavior].grid(row=i*2+1, column=3)

        tk.Button(master, text="Save Results", command=self.save_results, bg='lightgreen').grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Reset", command=self.reset_all, bg='salmon').grid(row=6, column=2, columnspan=2, pady=10)

        self.held_keys = set()

        master.bind('<KeyPress>', self.on_key_press)
        master.bind('<KeyRelease>', self.on_key_release)

    def increment_frequency(self, behavior):
        self.frequency_counts[behavior] += 1
        self.freq_labels[behavior].config(text=f"Frequency: {self.frequency_counts[behavior]}")

    def start_hold(self, behavior):
        if behavior not in self.hold_start_times:
            self.hold_start_times[behavior] = time.time()

    def end_hold(self, behavior):
        if behavior in self.hold_start_times:
            duration = time.time() - self.hold_start_times[behavior]
            self.duration_totals[behavior] += duration
            self.dur_labels[behavior].config(text=f"{self.duration_totals[behavior]:.2f} s")
            del self.hold_start_times[behavior]

    def save_results(self):
        default_filename = f"behavior_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=default_filename,
            title="Save Results As"
        )

        if not filepath:
            return  # user cancelled

        try:
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Behavior', 'Frequency', 'Total Duration (s)'])
                for behavior in self.behaviors:
                    writer.writerow([
                        behavior,
                        self.frequency_counts[behavior],
                        f"{self.duration_totals[behavior]:.2f}"
                    ])
            messagebox.showinfo("Saved", f"Results saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def reset_all(self):
        for behavior in self.behaviors:
            self.frequency_counts[behavior] = 0
            self.duration_totals[behavior] = 0.0
            self.freq_labels[behavior].config(text="Frequency: 0")
            self.dur_labels[behavior].config(text="0.00 s")

    def on_key_press(self, event):
        key = event.keysym.lower()

        if key in self.held_keys:
            return
        self.held_keys.add(key)

        if key == 'q':
            self.increment_frequency('Moving')
        elif key == 'w':
            self.increment_frequency('Grooming')
        elif key == 'p':
            self.increment_frequency('Rearing')
        elif key == 'a':
            self.start_hold('Moving')
        elif key == 's':
            self.start_hold('Grooming')
        elif key == 'l':
            self.start_hold('Rearing')

    def on_key_release(self, event):
        key = event.keysym.lower()
        self.held_keys.discard(key)

        if key == 'a':
            self.end_hold('Moving')
        elif key == 's':
            self.end_hold('Grooming')
        elif key == 'l':
            self.end_hold('Rearing')

if __name__ == "__main__":
    root = tk.Tk()
    app = BehaviorCounterApp(root)
    root.mainloop()
