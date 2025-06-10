import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import requests
import io


BACKEND_URL = 'http://127.0.0.1:5000'

face_img = None
voice_data = None


def capture_face():
    global face_img
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access webcam.")
        return
    messagebox.showinfo("Info", "Press 's' to capture face, 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Capture Face', frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            face_img = frame.copy()
            cv2.imwrite('face.jpg', face_img)
            messagebox.showinfo("Info", "Face captured!")
            break
        elif key & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def record_voice():
    global voice_data
    fs = 16000  # Sample rate
    duration = 3  # seconds
    messagebox.showinfo("Info", "Recording voice for 3 seconds...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        voice_data = np.squeeze(recording)
        wav.write('voice.wav', fs, voice_data)
        messagebox.showinfo("Info", "Voice recorded!")
    except Exception as e:
        messagebox.showerror("Error", f"Voice recording failed: {e}")

def register():
    print("Registering with captured face and voice...")

    global face_img, voice_data
    if face_img is None or voice_data is None:
        messagebox.showerror("Error", "Please capture face and record voice first.")
        return
    else:
        messagebox.showinfo("Info", "Registering with captured face and voice...")
    
    # Save face image and voice data to files
    cv2.imwrite('face.jpg', face_img)
    wav.write('voice.wav', 16000, voice_data)

    # Send files to backend for registration
    try:
        with open('face.jpg', 'rb') as f_img, open('voice.wav', 'rb') as f_voice:
            files = {'face': f_img, 'voice': f_voice}
            print("Sending registration request to backend...")
            print(f"Files: {files.keys()}")
            print(f"Backend URL: {BACKEND_URL}/register")
            print("Files ready for upload.")
            print("Sending POST request...")
            print("Files:", files)
            print("Waiting for response...")
            response = requests.post(f"{BACKEND_URL}/register", files=files)
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Registered! Response: {response.json()}")
        else:
            messagebox.showerror("Error", f"Registration failed: {response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"Registration error: {e}")

def verify():
    if face_img is None or voice_data is None:
        messagebox.showerror("Error", "Please capture face and record voice first.")
        return
    try:
        with open('face.jpg', 'rb') as f_img, open('voice.wav', 'rb') as f_voice:
            files = {'face': f_img, 'voice': f_voice}
            response = requests.post(f"{BACKEND_URL}/verify", files=files)
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Verification result: {response.json()}")
        else:
            messagebox.showerror("Error", f"Verification failed: {response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"Verification error: {e}")

root = tk.Tk()
root.title("SolChain Digital ID")

# Add buttons and UI elements for registration and verification
tk.Button(root, text="Capture Face", command=capture_face).pack(pady=5)
tk.Button(root, text="Record Voice", command=record_voice).pack(pady=5)
tk.Button(root, text="Register", command=register).pack(pady=5)
tk.Button(root, text="Verify", command=verify).pack(pady=5)

root.mainloop()
