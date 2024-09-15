import tkinter as tk
from tkinter import messagebox, filedialog
import speech_recognition as sr
import threading

# Initialize the recognizer
r = sr.Recognizer()

# Function to capture speech and recognize it
def recognize_speech(language):
    try:
        with sr.Microphone() as source:
            # Update the status label
            status_label.config(text="Calibrating mic for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=5)  # Adjust for ambient noise
            
            # Update status to notify the user to speak
            status_label.config(text="Say something!")
            audio = r.listen(source)  # Listen for audio input
            
            # Recognize the speech using Google Web Speech API
            text = r.recognize_google(audio, language=language)
            
            # Display the recognized text
            result_text.insert(tk.END, "You said: " + text + "\n")
            status_label.config(text="Recognition complete.")
    
    except sr.RequestError as e:
        # Handle API errors
        status_label.config(text="Error connecting to recognition service.")
        messagebox.showerror("Error", f"Could not request results; {e}")
    
    except sr.UnknownValueError:
        # Handle speech recognition failure
        status_label.config(text="Couldn't understand the audio.")
        messagebox.showerror("Error", "Sorry, I could not understand the audio.")

    except Exception as e:
        status_label.config(text="An error occurred.")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to run recognition in a background thread
def run_recognition_in_background():
    selected_language = language_var.get()
    lang_dict = {"English": "en-US", "Urdu": "ur-PK"}
    threading.Thread(target=recognize_speech, args=(lang_dict[selected_language],)).start()

# Function to save the transcription
def save_transcription():
    text = result_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text)
        messagebox.showinfo("Success", "Transcription saved!")

# Function to switch between dark and light mode
def toggle_theme():
    if theme_var.get():
        root.config(bg="#2c3e50")
        result_text.config(bg="#34495e", fg="white")
        status_label.config(bg="#2c3e50", fg="white")
    else:
        root.config(bg="white")
        result_text.config(bg="white", fg="black")
        status_label.config(bg="white", fg="black")

# Initialize the main window
root = tk.Tk()
root.title("Speech to Text")
root.geometry("500x500")

# Set up theme variables
theme_var = tk.BooleanVar(value=False)

# Header Frame for title and theme toggle
header_frame = tk.Frame(root)
header_frame.pack(pady=10)

title_label = tk.Label(header_frame, text="Speech Recognition App", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, padx=10)

theme_button = tk.Checkbutton(header_frame, text="Dark Mode", variable=theme_var, onvalue=True, offvalue=False, command=toggle_theme)
theme_button.grid(row=0, column=1)

# Create language selection dropdown
language_var = tk.StringVar(value="English")
language_label = tk.Label(root, text="Select Language:", font=("Helvetica", 12))
language_label.pack(pady=5)

language_menu = tk.OptionMenu(root, language_var, "English", "Urdu")
language_menu.pack()

# Create recording button
record_button = tk.Button(root, text="Start Recording", font=("Helvetica", 12), command=run_recognition_in_background, bg="#1abc9c", fg="white")
record_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Press the button and start speaking...", font=("Helvetica", 12))
status_label.pack(pady=5)

# Create text widget to display results
result_text = tk.Text(root, font=("Helvetica", 12), wrap="word", height=10, width=50)
result_text.pack(pady=10)

# Save Button
save_button = tk.Button(root, text="Save Transcription", font=("Helvetica", 12), command=save_transcription, bg="#3498db", fg="white")
save_button.pack(pady=10)

# Run the Tkinter event loop
root.config(bg="white")
root.mainloop()
