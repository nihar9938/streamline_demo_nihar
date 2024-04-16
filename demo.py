import win32com.client
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def send_meeting():
    subject = subject_entry.get()
    start_time = datetime.strptime(start_entry.get(), '%Y-%m-%d %H:%M')
    duration = int(duration_entry.get())
    location = location_entry.get()
    recipient_email = email_entry.get()

    outlook = win32com.client.Dispatch("Outlook.Application")
    meeting = outlook.CreateItem(1)  # 1 represents a calendar appointment (meeting)

    meeting.Subject = subject
    meeting.Start = start_time
    meeting.Duration = duration
    meeting.Location = location

    meeting.Recipients.Add(recipient_email)
    meeting.Recipients.ResolveAll()

    meeting.Send()

    messagebox.showinfo("Success", "Meeting invitation sent successfully!")

# Create GUI
root = tk.Tk()
root.title("Outlook Meeting Invitation")

# Labels and Entries
tk.Label(root, text="Subject:").pack()
subject_entry = tk.Entry(root)
subject_entry.pack()

tk.Label(root, text="Start Time (YYYY-MM-DD HH:MM):").pack()
start_entry = tk.Entry(root)
start_entry.pack()

tk.Label(root, text="Duration (minutes):").pack()
duration_entry = tk.Entry(root)
duration_entry.pack()

tk.Label(root, text="Location:").pack()
location_entry = tk.Entry(root)
location_entry.pack()

tk.Label(root, text="Recipient Email:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

# Send Button
send_button = tk.Button(root, text="Send Meeting Invitation", command=send_meeting)
send_button.pack()

root.mainloop()
