# NapMap - Sleep Debt Analyzer by Sohraab Singh Dhillon for NIELIT, Chandigarh
# This program helps users track their sleep patterns, analyze sleep debt, and visualize trends.
# This program uses Python's Tkinter for GUI, Pandas for data handling, and Seaborn/Matplotlib for visualization.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------
# Initialize DataFrame
# ----------------------
data = []
df = pd.DataFrame(columns=['date', 'sleep_time', 'wake_time'])

# ----------------------
# Helper Functions
# ----------------------
def update_dataframe(date, sleep_time, wake_time):
    global df
    try:
        sleep_datetime = pd.to_datetime(f"{date} {sleep_time}")
        wake_datetime = pd.to_datetime(f"{date} {wake_time}")
        if wake_datetime < sleep_datetime:
            wake_datetime += pd.Timedelta(days=1)
        sleep_hours = (wake_datetime - sleep_datetime).total_seconds() / 3600

        new_row = pd.DataFrame({
            'date': [pd.to_datetime(date)],
            'sleep_time': [sleep_time],
            'wake_time': [wake_time],
            'sleep_datetime': [sleep_datetime],
            'wake_datetime': [wake_datetime],
            'sleep_hours': [sleep_hours]
        })

        df = pd.concat([df, new_row], ignore_index=True)
        messagebox.showinfo("Success", "Sleep data added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def analyze_sleep():
    if df.empty:
        messagebox.showwarning("No Data", "Please enter some sleep records first.")
        return

    IDEAL_SLEEP_HOURS = 8
    df['sleep_debt'] = IDEAL_SLEEP_HOURS - df['sleep_hours']
    df['sleep_debt'] = df['sleep_debt'].apply(lambda x: x if x > 0 else 0)

    avg_sleep = df['sleep_hours'].mean()
    std_sleep = df['sleep_hours'].std()
    total_debt = df['sleep_debt'].sum()

    report = f"Average Sleep: {avg_sleep:.2f} hrs\n"
    report += f"Total Sleep Debt: {total_debt:.2f} hrs\n"
    report += f"Consistency (std dev): {std_sleep:.2f} hrs\n"

    if avg_sleep < 7:
        report += "⚠️ You're averaging less than 7 hours of sleep. Try going to bed earlier.\n"
    elif avg_sleep > 9:
        report += "😴 You're oversleeping. Monitor fatigue levels.\n"
    else:
        report += "✅ Your sleep duration is healthy.\n"

    if std_sleep > 1.5:
        report += "⚠️ Your sleep schedule is inconsistent. Try to fix a regular bedtime."
    else:
        report += "✅ Your sleep timing is consistent."

    report_text.delete(1.0, tk.END)
    report_text.insert(tk.END, report)

def plot_sleep_trend():
    if df.empty:
        messagebox.showwarning("No Data", "Enter some sleep records first.")
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=df, x='date', y='sleep_hours', marker='o', ax=ax)
    ax.axhline(8, color='r', linestyle='--', label='Ideal Sleep (8 hrs)')
    ax.set_title("Daily Sleep Duration")
    ax.set_ylabel("Hours Slept")
    ax.set_xlabel("Date")
    ax.legend()
    ax.grid(True)

    show_plot(fig)

def plot_heatmap():
    if df.empty:
        messagebox.showwarning("No Data", "Enter some sleep records first.")
        return

    df['sleep_hour'] = df['sleep_datetime'].dt.hour + df['sleep_datetime'].dt.minute / 60
    df['wake_hour'] = df['wake_datetime'].dt.hour + df['wake_datetime'].dt.minute / 60

    heatmap_data = pd.DataFrame({
        'Bedtime': df['sleep_hour'],
        'Wake Time': df['wake_hour']
    }, index=df['date'])

    fig, ax = plt.subplots(figsize=(8, 3))
    sns.heatmap(heatmap_data.T, cmap='coolwarm', ax=ax, cbar_kws={'label': 'Hour of Day'})
    ax.set_title("Sleep and Wake Times Heatmap")

    show_plot(fig)

def show_plot(fig):
    top = tk.Toplevel(root)
    top.title("Visualization")
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ----------------------
# GUI Setup
# ----------------------
root = tk.Tk()
root.title("Sleep Scheduler & Optimizer")
root.geometry("600x500")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Date
ttk.Label(frame, text="Date:").grid(row=0, column=0, sticky='e')
date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=0, column=1)

# Sleep time
ttk.Label(frame, text="Sleep Time (HH:MM):").grid(row=1, column=0, sticky='e')
sleep_entry = ttk.Entry(frame)
sleep_entry.grid(row=1, column=1)

# Wake time
ttk.Label(frame, text="Wake Time (HH:MM):").grid(row=2, column=0, sticky='e')
wake_entry = ttk.Entry(frame)
wake_entry.grid(row=2, column=1)

# Submit Button
submit_btn = ttk.Button(frame, text="Add Entry", command=lambda: update_dataframe(
    date_entry.get(), sleep_entry.get(), wake_entry.get()
))
submit_btn.grid(row=3, column=1, pady=10)

# Report Box
ttk.Label(frame, text="Sleep Report:").grid(row=4, column=0, sticky='nw', pady=5)
report_text = tk.Text(frame, width=50, height=8, wrap=tk.WORD)
report_text.grid(row=4, column=1, pady=5)

# Buttons
analyze_btn = ttk.Button(frame, text="Generate Report", command=analyze_sleep)
analyze_btn.grid(row=5, column=1, pady=5)

plot1_btn = ttk.Button(frame, text="Plot Sleep Trend", command=plot_sleep_trend)
plot1_btn.grid(row=6, column=1, pady=5)

plot2_btn = ttk.Button(frame, text="Plot Heatmap", command=plot_heatmap)
plot2_btn.grid(row=7, column=1, pady=5)

root.mainloop()
