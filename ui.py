# ui.py

import tkinter as tk
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
    style.theme_use("clam")

style = ttk.Style(root)  # Create a style instance
root.title("Adorable Chatbot")

# Global theme variable (Light by default)
theme_var = tk.StringVar(value="Light")

#####################################
# Initialize Message Handler & LLM
#####################################
# Save the default system prompt for later use.
default_system_prompt = "You are an expert actor that can fully immerse yourself into any role given. You do not break character for any reason, even if someone tries addressing you as an AI or language model. Currently your role is {{char}}, which is described in detail below. As {{char}}, continue the exchange with {{user}}."
message_handler = MessageHandler()  # assumes __init__ uses default_system_prompt
llm = LLM()

#####################################
# Custom Title Bar (for windows)
#####################################
def add_custom_title_bar(window, title_text):
    window.overrideredirect(True)
    title_bar = tk.Frame(window, bg="#2e2e2e", relief="raised", bd=0)
    title_bar.pack(fill=tk.X)
    title_label = tk.Label(title_bar, text=title_text, bg="#2e2e2e", fg="#d3d3d3", font=("Segoe UI", 12, "bold"))
    title_label.pack(side=tk.LEFT, padx=5)
    close_button = tk.Button(title_bar, text="✕", command=window.destroy, bg="#2e2e2e", fg="#d3d3d3", bd=0, highlightthickness=0)
    close_button.pack(side=tk.RIGHT, padx=5)
    
    def start_move(event):
        window._drag_x = event.x
        window._drag_y = event.y
    def on_move(event):
        x = event.x_root - window._drag_x
        y = event.y_root - window._drag_y
        window.geometry(f"+{x}+{y}")
    title_bar.bind("<ButtonPress-1>", start_move)
    title_bar.bind("<B1-Motion>", on_move)
    
    def on_focus_in(event):
        title_bar.config(bg="#2e2e2e")
        title_label.config(bg="#2e2e2e", fg="#d3d3d3")
    def on_focus_out(event):
        title_bar.config(bg="#3a3a3a")
        title_label.config(bg="#3a3a3a", fg="#d3d3d3")
    window.bind("<FocusIn>", on_focus_in)
    window.bind("<FocusOut>", on_focus_out)
    
    return title_bar, title_label

main_title_bar, main_title_label = add_custom_title_bar(root, "Adorable Chatbot")

#####################################
# Layout: Container, Sidebar, Main Frame
#####################################
container = ttk.Frame(root)
container.pack(fill=tk.BOTH, expand=True)

# Main frame (chat area) in column 1
main_frame = ttk.Frame(container)
main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
container.columnconfigure(1, weight=1)
container.rowconfigure(0, weight=1)

# Sidebar frame for settings (initially hidden) in column 0
sidebar_frame = ttk.Frame(container, width=250, relief=tk.RIDGE, padding=10)
sidebar_visible = False
def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar_frame.grid_forget()
        sidebar_visible = False
    else:
        sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        sidebar_visible = True

#####################################
# Settings Window with Theme Options
#####################################
settings_window = None
settings_title_bar = None
def open_settings():
    global settings_window, settings_title_bar
    settings_window = tk.Toplevel(root)
    settings_window.geometry("400x300")
    settings_title_bar, _ = add_custom_title_bar(settings_window, "Bot Settings")
    settings_window.configure(bg="white" if theme_var.get() == "Light" else "#2e2e2e")
    theme_frame = ttk.LabelFrame(settings_window, text="Theme", padding=10)
    theme_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    theme_label = ttk.Label(theme_frame, text="Select Theme:", font=("Segoe UI", 10))
    theme_label.pack(anchor="w", pady=(0,5))
    
    def change_theme():
        new_theme = theme_var.get()
        if new_theme == "Light":
            if hasattr(root, "set_theme"):
                root.set_theme("arc")
            else:
                style.theme_use("clam")
        else:
            if hasattr(root, "set_theme"):
                root.set_theme("equilux")
            else:
                style.theme_use("alt")
        # Update colors
        if new_theme == "Dark":
            update_chat_theme(bg="#2e2e2e", fg="#d3d3d3")
            header_label.config(bg="#2e2e2e", fg="#d3d3d3")
            settings_window.config(bg="#2e2e2e")
            prompt_text.config(bg="#2e2e2e", fg="#d3d3d3", insertbackground="#d3d3d3")
            initial_ai_text.config(bg="#2e2e2e", fg="#d3d3d3", insertbackground="#d3d3d3")
        else:
            update_chat_theme(bg="white", fg="black")
            header_label.config(bg="white", fg="black")
            settings_window.config(bg="white")
            prompt_text.config(bg="white", fg="black", insertbackground="black")
            initial_ai_text.config(bg="white", fg="black", insertbackground="black")
    
    ttk.Radiobutton(theme_frame, text="Light", variable=theme_var, value="Light", command=change_theme).pack(anchor="w")
    ttk.Radiobutton(theme_frame, text="Dark", variable=theme_var, value="Dark", command=change_theme).pack(anchor="w")
    placeholder_label = ttk.Label(settings_window, text="Other settings will go here.", font=("Segoe UI", 12))
    placeholder_label.pack(pady=(0,20), padx=20)
    change_theme()

#####################################
# Character Manager Window (New!)
#####################################
def open_character_manager():
    # Create a new Toplevel window for character creation
    char_window = tk.Toplevel(root)
    char_window.geometry("400x400")
    add_custom_title_bar(char_window, "Character Manager")
    char_window.configure(bg="white" if theme_var.get() == "Light" else "#2e2e2e")
    
    # Label and text box for Character Description
    desc_label = ttk.Label(char_window, text="Character Description:", font=("Segoe UI", 10, "bold"))
    desc_label.pack(anchor="w", padx=10, pady=(10,0))
    desc_text = tk.Text(char_window, height=6, width=40, font=("Segoe UI", 10))
    desc_text.pack(padx=10, pady=(0,10))
    
    # Label and text box for Initial Message
    init_label = ttk.Label(char_window, text="Initial Message:", font=("Segoe UI", 10, "bold"))
    init_label.pack(anchor="w", padx=10, pady=(10,0))
    init_text = tk.Text(char_window, height=4, width=40, font=("Segoe UI", 10))
    init_text.pack(padx=10, pady=(0,10))
    
    # Button to start a new chat with this custom character
    def start_character_chat():
        description = desc_text.get("1.0", tk.END).strip()
        initial_message = init_text.get("1.0", tk.END).strip()
        if not description or not initial_message:
            return  # Require both fields
        # Create a new system prompt by appending the character description to the default system prompt.
        new_system = default_system_prompt + "\n" + description
        # Reset conversation
        message_handler.conversation = []
        message_handler.conversation.append(("system", new_system))
        message_handler.conversation.append(("assistant", initial_message))
        # Clear the chat area
        for widget in chat_frame.winfo_children():
            widget.destroy()
        # Add the initial message bubble
        add_message_bubble("assistant", "Bot: " + initial_message)
        char_window.destroy()
    ttk.Button(char_window, text="Start Chat with Character", command=start_character_chat).pack(pady=10)

#####################################
# Header and Control Buttons (Above Chat Area)
#####################################
header_frame = ttk.Frame(main_frame)
header_frame.pack(side=tk.TOP, fill=tk.X)
hamburger_button = ttk.Button(header_frame, text="☰", command=toggle_sidebar)
hamburger_button.pack(side=tk.LEFT, padx=(0, 5))
cog_button = ttk.Button(header_frame, text="⚙", command=open_settings)
cog_button.pack(side=tk.LEFT, padx=(0,5))
# New character manager button with an icon (using 👤)
char_button = ttk.Button(header_frame, text="👤", command=open_character_manager)
char_button.pack(side=tk.LEFT, padx=(0,5))
header_label = tk.Label(header_frame, text="Adorable Chatbot", font=("Segoe UI", 16, "bold"), bg="white", fg="black")
header_label.pack(side=tk.LEFT, padx=10, pady=5)

#####################################
# Chat Area as a Messaging App (Message Bubbles)
#####################################
chat_container = ttk.Frame(main_frame)
chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
chat_canvas = tk.Canvas(chat_container, borderwidth=0, highlightthickness=0)
chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=chat_canvas.yview, style="Vertical.TScrollbar")
chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_canvas.configure(yscrollcommand=chat_scrollbar.set)
chat_frame = ttk.Frame(chat_canvas)
chat_window = chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
def on_frame_configure(event):
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
chat_frame.bind("<Configure>", on_frame_configure)
def update_chat_theme(bg, fg):
    chat_canvas.config(bg=bg)
    chat_frame.config(style="Chat.TFrame")
    for child in chat_frame.winfo_children():
        if hasattr(child, "role"):
            if child.role == "human":
                child.config(bg=bg)
                child.label.config(bg="#dcf8c6" if bg=="white" else "#3e3e3e", fg=fg)
            elif child.role in ("assistant", "system"):
                child.config(bg=bg)
                child.label.config(bg="#ffffff" if bg=="white" else "#4e4e4e", fg=fg)

#####################################
# Function to Add Message Bubbles
#####################################
def add_message_bubble(role, message):
    # Create a full-width container frame for alignment.
    bubble_container = tk.Frame(chat_frame, bg=chat_canvas.cget("bg"))
    bubble_container.pack(fill="x", pady=5)
    
    bubble = tk.Frame(bubble_container, bg=chat_canvas.cget("bg"), padx=5, pady=5)
    bubble.role = role
    if theme_var.get() == "Dark":
        bubble_bg = "#3e3e3e" if role == "human" else "#4e4e4e"
    else:
        bubble_bg = "#dcf8c6" if role == "human" else "#ffffff"
    bubble.label = tk.Label(bubble, text=message, bg=bubble_bg, wraplength=300, justify="left", font=("Segoe UI", 10))
    bubble.label.pack(padx=10, pady=5)
    
    # Align bubble: if human, pack to the right; otherwise, pack to the left.
    if role == "human":
        bubble.pack(side="right", padx=10)
    else:
        bubble.pack(side="left", padx=10)
    
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)

#####################################
# Sidebar Content for Updating Prompts
#####################################
prompt_label = ttk.Label(sidebar_frame, text="System Prompt:", font=("Segoe UI", 10, "bold"))
prompt_label.pack(anchor="w")
prompt_text = tk.Text(sidebar_frame, height=5, width=30, font=("Segoe UI", 10))
prompt_text.insert(tk.END, message_handler.get_conversation()[0][1])
prompt_text.pack(pady=(0,10))
update_prompt_button = ttk.Button(sidebar_frame, text="Update Prompt", command=lambda: update_prompt())
update_prompt_button.pack(pady=(0,10))
initial_ai_label = ttk.Label(sidebar_frame, text="Initial AI Message:", font=("Segoe UI", 10, "bold"))
initial_ai_label.pack(anchor="w")
initial_ai_text = tk.Text(sidebar_frame, height=5, width=30, font=("Segoe UI", 10))
default_initial_ai = message_handler.get_conversation()[1][1] if len(message_handler.get_conversation()) > 1 else ""
initial_ai_text.insert(tk.END, default_initial_ai)
initial_ai_text.pack(pady=(0,10))
update_initial_ai_button = ttk.Button(sidebar_frame, text="Update Initial AI Message", command=lambda: update_initial_ai_message())
update_initial_ai_button.pack(pady=(0,10))

#####################################
# Input Area for Sending Messages
#####################################
input_frame = ttk.Frame(main_frame)
input_frame.pack(fill=tk.X, padx=10, pady=(0,10))
entry = ttk.Entry(input_frame, width=60, font=("Segoe UI", 10))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", lambda event: send_message())
send_button = ttk.Button(input_frame, text="Send", command=lambda: send_message())
send_button.pack(side=tk.LEFT, padx=5)

#####################################
# Message Sending and Response Handling
#####################################
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    message_handler.add_message("human", user_input)
    add_message_bubble("human", "You: " + user_input)
    entry.delete(0, tk.END)
    
    def fetch_response():
        try:
            ai_response_obj = llm.get_response(message_handler.get_conversation())
            ai_response = getattr(ai_response_obj, "content", str(ai_response_obj))
            message_handler.add_message("assistant", ai_response)
            chat_frame.after(0, lambda: add_message_bubble("assistant", "Bot: " + ai_response))
        except Exception as e:
            chat_frame.after(0, lambda: add_message_bubble("assistant", "Error: " + str(e)))
    threading.Thread(target=fetch_response).start()

def update_prompt():
    new_prompt = prompt_text.get("1.0", tk.END).strip()
    if new_prompt:
        message_handler.update_system_prompt(new_prompt)
        add_message_bubble("system", "System prompt updated!")

def update_initial_ai_message():
    new_message = initial_ai_text.get("1.0", tk.END).strip()
    if new_message:
        message_handler.update_initial_ai_message(new_message)
        add_message_bubble("system", "Initial AI message updated!")

root.mainloop()
