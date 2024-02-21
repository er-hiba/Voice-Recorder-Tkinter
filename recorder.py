import tkinter as tk
from tkinter import filedialog
from tkinter import font
import sounddevice as sd
import soundfile as sf
import time

# Global variables to keep track of recording state, audio data, and start time
recording = False
audio_data = None
start_time = None

# Set the default samplerate
sd.default.samplerate = 44100

# Function to toggle recording
def toggle_recording():
    global recording
    global audio_data
    global start_time

    if not recording:
        # Start recording
        start_time = time.time()
        recording = True
        start_button.config(text="Stop Recording", bg="#FFDAB9", fg="black")
        audio_data = sd.rec(5 * sd.default.samplerate, samplerate=sd.default.samplerate, channels=2, dtype="int16")
        start_timer()
    else:
        # Stop recording
        recording = False
        start_button.config(text="Start Recording", bg="#FFA07A",fg="white")
        sd.stop()
        sd.wait()
        save_button.config(state=tk.NORMAL)


# Function to update the recording timer
def start_timer():
    global start_time
    elapsed_time = time.time() - start_time
    timer_label.config(text=f"Recording : {int(elapsed_time)} seconds")
    if recording:
        timer_label.after(1000, start_timer)


# Function to save the recorded audio
def save_audio():
    global audio_data

    if audio_data is not None:
        # Ask user for file location and save the audio as a WAV file
        filename = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if filename:
            sf.write(filename, audio_data, samplerate=sd.default.samplerate)


# Create the main Tkinter window
root = tk.Tk()
root.geometry("500x600")
root.resizable(False, False)
root.title("Voice Recorder")
root.config(bg="#FEBAAD")

# Set the window icon
image_icon = tk.PhotoImage(file="icon.png")
root.iconphoto(True, image_icon)

# Set the logo image
photo = tk.PhotoImage(file="image.png")
myimage = tk.Label(image=photo, bg="#FEBAAD")
myimage.place(relx=0.48, rely=0.1, anchor="n")

# Load the custom font
font_path = "UnicornsAreAwesome-xdEq.ttf"
custom_font = font.Font(family="Unicorns are Awesome", size=40)

# Create a label with the custom font for the title
label = tk.Label(root, text="Voice Recorder", font=custom_font, bg="#FEBAAD",fg="#3B3024" )
label.place(relx=0.5, rely=0.02, anchor="n")

# Create the Save Audio button
save_button = tk.Button(root, text="Save Audio", font=(custom_font.actual()['family'], 20), bg="#F08080", fg="white",\
                        command=save_audio, state=tk.DISABLED, width=15)
save_button.place(x=150,y=480)

# Create the Start Recording button
start_button = tk.Button(root, text="Start Recording",font=(custom_font.actual()['family'], 20), command=toggle_recording,\
                         bg="#FFA07A",fg="white", width=15)
start_button.place(x=150,y=330)

# Create the recording timer label
timer_label = tk.Label(root, text="", font=(custom_font.actual()['family'], 32), bg="#FEBAAD", fg="#3B3024")
timer_label.place(x=105,y=400)

# Start the Tkinter event loop
root.mainloop()
