import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox

# ---------------- MOOD DETECTION ---------------- #
def detect_mood():
    cap = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    detected_mood = "Neutral"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]

            brightness = np.mean(face)
            edges = cv2.Canny(face, 50, 150)
            edge_density = np.sum(edges) / (w * h)

            if brightness > 140:
                detected_mood = "Happy 😊"
            elif brightness < 90:
                detected_mood = "Sad 😢"
            elif edge_density > 0.15:
                detected_mood = "Angry 😡"
            else:
                detected_mood = "Neutral 😐"

            cap.release()
            cv2.destroyAllWindows()
            return detected_mood

        cv2.imshow("Detecting Mood...", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_mood


# ---------------- CHATBOT RESPONSE ---------------- #
def get_response(user_msg, mood):
    user_msg = user_msg.lower()

    # Exit condition
    if "bye" in user_msg:
        return "Goodbye! Take care 💙"

    # Greetings
    if "hi" in user_msg or "hello" in user_msg:
        return "Hello! I'm here for you 😊"

    # Thank you
    if "thank" in user_msg:
        return "You're always welcome 💙"

    # Sadness help
    if "sad" in user_msg or "depressed" in user_msg:
        return "I'm sorry you're feeling this way 💙 Try talking to someone you trust or doing something you enjoy."

    # Stress / anxiety
    if "stress" in user_msg or "anxiety" in user_msg:
        return "Take deep breaths 🧘 Try to relax your mind. You can handle this."

    # Motivation
    if "motivate" in user_msg or "motivation" in user_msg:
        return "You are stronger than you think 💪 Keep going!"

    # Help question
    if "how" in user_msg:
        return "That's a great question 🙂 Try small steps, stay consistent, and be kind to yourself."

    # Default based on mood
    if "sad" in mood.lower():
        return "I understand... things will get better 💙"

    elif "happy" in mood.lower():
        return "That's great! Keep smiling 😊"

    elif "angry" in mood.lower():
        return "Try to calm down 😌 Take a break and breathe slowly."

    else:
        return "Tell me more about how you're feeling 🙂"
# ---------------- UI APP ---------------- #
def start_app():
    global mood

    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()

    if not name or not age or not gender:
        messagebox.showerror("Error", "Please fill all details")
        return

    mood = detect_mood()

    chat_box.insert(tk.END, f"\nSystem: Mood detected → {mood}\n")
    chat_box.insert(tk.END, f"Bot: Hello {name}! How are you feeling today?\n")


def send_message():
    user_msg = entry.get()

    if user_msg == "":
        return

    chat_box.insert(tk.END, f"You: {user_msg}\n")

    response = get_response(user_msg, mood)
    chat_box.insert(tk.END, f"Bot: {response}\n")

    entry.delete(0, tk.END)

    if "bye" in user_msg.lower():
        root.quit()


# ---------------- MAIN WINDOW ---------------- #
root = tk.Tk()
root.title("AI Mental Health Chatbot")
root.geometry("500x600")

# User details
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Gender").pack()
gender_entry = tk.Entry(root)
gender_entry.pack()

tk.Button(root, text="Start Camera & Detect Mood", command=start_app).pack(pady=10)

# Chat area
chat_box = tk.Text(root, height=20, width=60)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=10)

tk.Button(root, text="Send", command=send_message).pack(side=tk.LEFT)

root.mainloop()