# ui.py

import tkinter as tk
from tkinter import scrolledtext
import threading
import tkinter.ttk as ttk
from message_handler import MessageHandler
from llm import LLM

# Try to use ThemedTk from ttkthemes for a modern look; fallback if not installed
try:
    from ttkthemes import ThemedTk
    root = ThemedTk(theme="arc")
except ImportError:
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')

root.title("Adorable Chatbot")

# Create a container frame using grid layout for sidebar and main content
container = ttk.Frame(root)
container.pack(fill=tk.BOTH, expand=True)

# Create main frame for chat in column 1
main_frame = ttk.Frame(container)
main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
container.columnconfigure(1, weight=1)
container.rowconfigure(0, weight=1)

# Sidebar frame for settings, initially hidden; will be placed in column 0
sidebar_frame = ttk.Frame(container, width=250, relief=tk.RIDGE, padding=10)

# Toggle sidebar visibility (opens on the left)
sidebar_visible = False
def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar_frame.grid_forget()
        sidebar_visible = False
    else:
        sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        sidebar_visible = True

# Function to open a new settings window (currently empty)
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Bot Settings")
    settings_window.geometry("400x300")
    settings_label = ttk.Label(settings_window, text="Settings will go here.", font=("Segoe UI", 12))
    settings_label.pack(pady=20, padx=20)

# Initialize the message handler and LLM instances
message_handler = MessageHandler()
llm = LLM()

def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return  # No empty messages, darling!
    
    # Add user's message to conversation and update chat history
    message_handler.add_message("human", user_input)
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)
    
    # Fetch the LLM response in a separate thread
    def fetch_response():
        try:
            ai_response_obj = llm.get_response(message_handler.get_conversation())
            ai_response = getattr(ai_response_obj, "content", str(ai_response_obj))
            message_handler.add_message("assistant", ai_response)
            chat_history.after(0, lambda: chat_history.insert(tk.END, "Bot: " + ai_response + "\n"))
        except Exception as e:
            chat_history.after(0, lambda: chat_history.insert(tk.END, "Error: " + str(e) + "\n"))
    
    threading.Thread(target=fetch_response).start()

def update_prompt():
    new_prompt = prompt_text.get("1.0", tk.END).strip()
    if not new_prompt:
        return  # Don't update to an empty prompt, babe!
    message_handler.update_system_prompt(new_prompt)
    chat_history.insert(tk.END, "System prompt updated!\n")

def update_initial_ai_message():
    new_message = initial_ai_text.get("1.0", tk.END).strip()
    if not new_message:
        return  # No empty updates, darling!
    message_handler.update_initial_ai_message(new_message)
    chat_history.insert(tk.END, "Initial AI message updated!\n")

# Create a control frame with a hamburger button and a cog button in the main frame
control_frame = ttk.Frame(main_frame)
control_frame.pack(side=tk.TOP, fill=tk.X)
hamburger_button = ttk.Button(control_frame, text="☰", command=toggle_sidebar)
hamburger_button.pack(side=tk.LEFT, padx=(0, 5))
cog_button = ttk.Button(control_frame, text="⚙", command=open_settings)
cog_button.pack(side=tk.LEFT)

# Chat history widget in the main frame
chat_history = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=20, font=("Segoe UI", 10))
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
initial_ai_message = message_handler.get_conversation()[1][1] if len(message_handler.get_conversation()) > 1 else ""
chat_history.insert(tk.END, "Bot: " + initial_ai_message + "\n")

# Entry widget and send button for user messages in the main frame
entry = ttk.Entry(main_frame, width=60, font=("Segoe UI", 10))
entry.pack(padx=10, pady=(0,10), fill=tk.X)
entry.bind("<Return>", lambda event: send_message())
send_button = ttk.Button(main_frame, text="Send", command=send_message)
send_button.pack(padx=10, pady=(0,10))

# Sidebar content: System prompt update section
prompt_label = ttk.Label(sidebar_frame, text="System Prompt:", font=("Segoe UI", 10, "bold"))
prompt_label.pack(anchor="w")
prompt_text = tk.Text(sidebar_frame, height=5, width=30, font=("Segoe UI", 10))
default_prompt = message_handler.get_conversation()[0][1]
prompt_text.insert(tk.END, default_prompt)
prompt_text.pack(pady=(0,10))
update_prompt_button = ttk.Button(sidebar_frame, text="Update Prompt", command=update_prompt)
update_prompt_button.pack(pady=(0,10))

# Sidebar content: Initial AI Message update section
initial_ai_label = ttk.Label(sidebar_frame, text="Initial AI Message:", font=("Segoe UI", 10, "bold"))
initial_ai_label.pack(anchor="w")
initial_ai_text = tk.Text(sidebar_frame, height=5, width=30, font=("Segoe UI", 10))
default_initial_ai = message_handler.get_conversation()[1][1] if len(message_handler.get_conversation()) > 1 else ""
initial_ai_text.insert(tk.END, default_initial_ai)
initial_ai_text.pack(pady=(0,10))
update_initial_ai_button = ttk.Button(sidebar_frame, text="Update Initial AI Message", command=update_initial_ai_message)
update_initial_ai_button.pack(pady=(0,10))

root.mainloop()
