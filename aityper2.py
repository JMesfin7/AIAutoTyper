import tkinter as tk
import time
import threading
import pyautogui
from openai import OpenAI

# --- Configuration ---
client = OpenAI(api_key= "OPENAI_API_KEY")
# --- Typing Control ---
typing_canceled = False

def cancel_typing():
    global typing_canceled
    typing_canceled = True

def type_text(text, typing_speed):
    global typing_canceled
    typing_canceled = False

    delay = 60 / typing_speed  # seconds per word (WPM)
    for char in text:
        if typing_canceled:
            break
        pyautogui.write(char)
        time.sleep(delay / 5)  # Approximate: 5 chars per word

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def on_generate_click():
    prompt = prompt_entry.get("1.0", tk.END).strip()
    try:
        typing_speed = int(speed_entry.get())
    except ValueError:
        status_label.config(text="Invalid typing speed.")
        return

    if not prompt:
        status_label.config(text="Prompt is empty.")
        return

    status_label.config(text="Switch to target window... typing starts in 3 seconds.")
    root.update()
    time.sleep(3)

    def thread_func():
        response = generate_response(prompt)
        type_text(response, typing_speed)
        status_label.config(text="✅ Done.")

    threading.Thread(target=thread_func).start()

def save_response():
    prompt = prompt_entry.get("1.0", tk.END).strip()
    if prompt:
        with open("saved_prompt.txt", "w") as f:
            f.write(prompt)
        status_label.config(text="Prompt saved!")
    else:
        status_label.config(text="Prompt is empty.")

# --- GUI Setup ---
root = tk.Tk()
root.title("AI Typer")
root.geometry("700x400")
root.configure(bg="#1e1e1e")

prompt_label = tk.Label(root, text="Enter your prompt:", fg="white", bg="#1e1e1e")
prompt_label.pack(pady=5)

prompt_entry = tk.Text(root, height=5, width=80, bg="#2e2e2e", fg="white")
prompt_entry.pack(pady=5)

speed_label = tk.Label(root, text="Typing Speed (Words Per Minute):", fg="white", bg="#1e1e1e")
speed_label.pack(pady=5)

speed_entry = tk.Entry(root, width=10, justify="center")
speed_entry.insert(0, "60")
speed_entry.pack(pady=5)

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

generate_button = tk.Button(button_frame, text="Generate & Type", command=on_generate_click, width=20)
generate_button.grid(row=0, column=0, padx=5)

cancel_button = tk.Button(button_frame, text="Cancel Typing", command=cancel_typing, width=15)
cancel_button.grid(row=0, column=1, padx=5)

save_button = tk.Button(button_frame, text="Save Prompt", command=save_response, width=15)
save_button.grid(row=0, column=2, padx=5)

status_label = tk.Label(root, text="", font=("Helvetica", 10), fg="blue", bg="#1e1e1e")
status_label.pack(pady=5)

# --- Run the GUI ---
if __name__ == "__main__":
    root.mainloop()