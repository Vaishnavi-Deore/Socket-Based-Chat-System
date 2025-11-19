import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
from datetime import datetime
import random
import time

# ========= USERNAME PROMPT =========
root = tk.Tk()
root.withdraw()
username = simpledialog.askstring("Hacker Login", "Enter your hacker name:")
if not username:
    username = "Anonymous"

# ========= CONNECT TO SERVER =========
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9999))

# ========= GLITCH EFFECT =========
def glitch_text(original):
    glitched = ""
    glitch_chars = "#$%&/=?!*@<>"
    for ch in original:
        if random.random() < 0.15:
            glitched += random.choice(glitch_chars)
        else:
            glitched += ch
    return glitched

# ========= MESSAGE FORMATTER =========
def format_message(raw_msg):
    try:
        username_raw, text = raw_msg.split(":", 1)
    except:
        return raw_msg

    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"[{timestamp}] <{username_raw.strip()}> {text.strip()}"

# ========= ASCII BANNER =========
BANNER_FRAMES = [
"""
 ███╗   ██╗███████╗██╗  ██╗
 ████╗  ██║██╔════╝██║ ██╔╝
 ██╔██╗ ██║█████╗  █████╔╝ 
 ██║╚██╗██║██╔══╝  ██╔═██╗ 
 ██║ ╚████║███████╗██║  ██╗
""",
"""
 ███╗   ██╗███████╗██╗  ██╗
 ██╔██╗ ██║██╔════╝██║ ██╔╝
 ██████╗██║█████╗  █████╔╝ 
 ██║╚██╗██║██╔══╝  ██╔═██╗ 
 ██║ ╚████║███████╗██║  ██╗
"""
]

# ========= GUI =========
win = tk.Tk()
win.title("Hacker Chat Terminal")
win.geometry("650x650")
win.configure(bg="black")
win.attributes("-alpha", 0.97)

banner_label = tk.Label(
    win, text=BANNER_FRAMES[0], fg="#00FF00",
    bg="black", font=("Consolas", 12)
)
banner_label.pack()

chat_box = scrolledtext.ScrolledText(
    win, bg="black", fg="#00FF00",
    font=("Consolas", 13), insertbackground="#00FF00",
    borderwidth=2, relief="flat"
)
chat_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
chat_box.config(state=tk.DISABLED)

chat_box.tag_config("timestamp", foreground="#00CC66")
chat_box.tag_config("message", foreground="#00FF00")

msg_entry = tk.Entry(
    win, bg="black", fg="#00FF00", font=("Consolas", 13),
    highlightthickness=2, highlightbackground="#00FF00", insertbackground="#00FF00"
)
msg_entry.pack(fill=tk.X, padx=10, pady=10)

# ========= BANNER ANIMATION =========
def animate_banner():
    i = 0
    while True:
        banner_label.config(text=BANNER_FRAMES[i % len(BANNER_FRAMES)])
        i += 1
        time.sleep(0.8)

threading.Thread(target=animate_banner, daemon=True).start()

# ========= RECEIVE MESSAGES =========
def receive():
    while True:
        try:
            raw_msg = sock.recv(1024).decode()
            if not raw_msg:
                break

            msg = format_message(raw_msg)

            # Glitch animation
            for _ in range(2):
                glitched = glitch_text(msg)
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, glitched + "\r")
                chat_box.delete("end-2l", "end-1l")
                chat_box.config(state=tk.DISABLED)
                chat_box.yview(tk.END)
                time.sleep(0.05)

            # Final clean message
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, "-" * 60 + "\n", "timestamp")

            left = msg.split(">", 1)[0] + "> "
            right = msg.split(">", 1)[1]

            chat_box.insert(tk.END, left, "timestamp")
            chat_box.insert(tk.END, right + "\n", "message")

            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)

        except:
            break

# ========= SEND MESSAGE =========
def send_msg(event=None):
    msg = msg_entry.get()
    if msg.strip() == "":
        return

    final_message = f"{username}: {msg}"
    sock.send(final_message.encode())
    msg_entry.delete(0, tk.END)

msg_entry.bind("<Return>", send_msg)

# Start listening
threading.Thread(target=receive, daemon=True).start()

win.mainloop()
