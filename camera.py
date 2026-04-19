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
    smile_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_smile.xml'
    )
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml'
    )

    detected_mood = "Neutral 😐"
    mood_scores = {
        "Happy 😊": 0,
        "Angry 😡": 0,
        "Fear 😨": 0,
        "Sad 😢": 0,
        "Neutral 😐": 0
    }

    frames_analyzed = 0
    max_frames = 60

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
        )

        for (x, y, w, h) in faces:
            face_gray = gray[y:y+h, x:x+w]
            face_eq   = cv2.equalizeHist(face_gray)

            # ---- Region slicing ----
            upper = face_eq[:h//2, :]
            lower = face_eq[h//2:, :]
            mouth = face_eq[int(h*0.65):, w//5:4*w//5]
            brow  = face_eq[:h//4, :]
            eye_region = face_eq[h//8:h//2, :]

            # ---- Smile detection (relaxed) ----
            smiles = smile_cascade.detectMultiScale(
                lower,
                scaleFactor=1.5,
                minNeighbors=8,      # lowered from 22 → catches real smiles
                minSize=(20, 10)
            )
            smile_detected = len(smiles) > 0

            # ---- Eye detection ----
            eyes = eye_cascade.detectMultiScale(
                eye_region,
                scaleFactor=1.1,
                minNeighbors=6,
                minSize=(15, 15)
            )
            eyes_open = len(eyes)

            # ---- Edge densities ----
            def edge_den(region):
                if region.size == 0:
                    return 0.0
                e = cv2.Canny(region, 30, 100)
                return np.sum(e > 0) / e.size

            ed_full  = edge_den(face_eq)
            ed_upper = edge_den(upper)
            ed_lower = edge_den(lower)
            ed_mouth = edge_den(mouth)
            ed_brow  = edge_den(brow)

            # ---- Variance (muscle tension) ----
            var_upper = float(np.var(upper.astype(np.float32)))
            var_lower = float(np.var(lower.astype(np.float32)))
            var_brow  = float(np.var(brow.astype(np.float32)))

            # ---- Brightness ----
            brightness = float(np.mean(face_eq))

            # ---- Debug print (remove after testing) ----
            print(f"smile={smile_detected} eyes={eyes_open} "
                  f"ed_full={ed_full:.3f} ed_upper={ed_upper:.3f} "
                  f"ed_lower={ed_lower:.3f} ed_mouth={ed_mouth:.3f} "
                  f"ed_brow={ed_brow:.3f} brightness={brightness:.1f} "
                  f"var_upper={var_upper:.1f} var_lower={var_lower:.1f}")

            # ======== MOOD DECISION ========

            # HAPPY — smile cascade fired OR lower face clearly more active
            if smile_detected:
                mood_scores["Happy 😊"] += 2   # strong signal, double weight

            elif ed_lower > ed_upper * 1.3 and ed_mouth > 0.08:
                mood_scores["Happy 😊"] += 1

            # ANGRY — brow very tense, upper dominates, no smile
            elif ed_brow > 0.15 and var_brow > 600 and ed_upper > ed_lower:
                mood_scores["Angry 😡"] += 1

            # FEAR — eyes wide, high full face tension
            elif eyes_open >= 2 and ed_full > 0.15 and ed_upper > 0.15:
                mood_scores["Fear 😨"] += 1

            # SAD — low energy face, relaxed/drooping, no smile
            elif ed_full < 0.13 and ed_mouth < 0.09 and var_lower < 500:
                mood_scores["Sad 😢"] += 1

            # NEUTRAL
            else:
                mood_scores["Neutral 😐"] += 1

            frames_analyzed += 1

        # ---- Camera overlay ----
        display = frame.copy()
        remaining = max_frames - frames_analyzed

        cv2.putText(display,
                    f"Analyzing... {remaining} frames left",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)

        if frames_analyzed > 0:
            leading = max(mood_scores, key=mood_scores.get)
            cv2.putText(display,
                        f"Leading: {leading}",
                        (10, 65), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (0, 255, 255), 2)

            # Show all scores on screen for debugging
            y_pos = 100
            for m, s in mood_scores.items():
                cv2.putText(display, f"{m}: {s}",
                            (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (200, 200, 255), 1)
                y_pos += 22

        cv2.imshow("Detecting Mood - Hold your expression", display)

        if frames_analyzed >= max_frames:
            detected_mood = max(mood_scores, key=mood_scores.get)
            break

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_mood


# ---------------- CHATBOT RESPONSE ---------------- #
def get_response(user_msg, mood):
    user_msg = user_msg.lower()

    if "bye" in user_msg:
        return "Goodbye! Take care 💙"

    if "hi" in user_msg or "hello" in user_msg:
        return "Hello! I'm here for you 😊"

    if "thank" in user_msg:
        return "You're always welcome 💙"

    if "sad" in user_msg or "depressed" in user_msg:
        return "I'm sorry you're feeling this way 💙 Try talking to someone you trust or doing something you enjoy."

    if "stress" in user_msg or "anxiety" in user_msg:
        return "Take deep breaths 🧘 Try to relax your mind. You can handle this."

    if "motivate" in user_msg or "motivation" in user_msg:
        return "You are stronger than you think 💪 Keep going!"

    if "scared" in user_msg or "fear" in user_msg or "afraid" in user_msg:
        return "It's okay to feel scared 💙 Take a deep breath — you are safe right now."

    if "angry" in user_msg or "frustrated" in user_msg:
        return "I hear you 💙 It's okay to feel angry. Try taking a short walk or breathing deeply."

    if "how" in user_msg:
        return "That's a great question 🙂 Try small steps, stay consistent, and be kind to yourself."

    if "happy" in mood.lower():
        return "That's wonderful! Keep smiling and spreading positivity 😊"

    elif "sad" in mood.lower():
        return "I understand... things will get better 💙 I'm here for you."

    elif "angry" in mood.lower():
        return "Try to calm down 😌 Take a break and breathe slowly."

    elif "fear" in mood.lower():
        return "It's okay to feel scared 💙 Take a deep breath — you are safe right now."

    else:
        return "Tell me more about how you're feeling 🙂"


# ---------------- UI APP ---------------- #
mood = "Neutral 😐"

def start_app():
    global mood

    name   = name_entry.get()
    age    = age_entry.get()
    gender = gender_entry.get()

    if not name or not age or not gender:
        messagebox.showerror("Error", "Please fill all details")
        return

    chat_box.insert(tk.END, "System: Starting camera... Hold your expression steady ⏳\n")
    root.update()

    mood = detect_mood()

    chat_box.insert(tk.END, f"System: Mood detected → {mood}\n")
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
root.title("AI Mental Health Therapist Chatbot")
root.geometry("500x650")
root.configure(bg="#f0f4f8")

tk.Label(root, text="🧠 AI Mental Health Therapist",
         font=("Helvetica", 14, "bold"),
         bg="#f0f4f8", fg="#2c3e50").pack(pady=8)

frame = tk.Frame(root, bg="#f0f4f8")
frame.pack()

tk.Label(frame, text="Name:",   bg="#f0f4f8").grid(row=0, column=0, sticky="e", padx=5, pady=3)
name_entry = tk.Entry(frame, width=25)
name_entry.grid(row=0, column=1, pady=3)

tk.Label(frame, text="Age:",    bg="#f0f4f8").grid(row=1, column=0, sticky="e", padx=5, pady=3)
age_entry = tk.Entry(frame, width=25)
age_entry.grid(row=1, column=1, pady=3)

tk.Label(frame, text="Gender:", bg="#f0f4f8").grid(row=2, column=0, sticky="e", padx=5, pady=3)
gender_entry = tk.Entry(frame, width=25)
gender_entry.grid(row=2, column=1, pady=3)

tk.Button(root, text="📷 Start Camera & Detect Mood",
          command=start_app,
          bg="#3498db", fg="white",
          font=("Helvetica", 10, "bold"),
          padx=10, pady=5).pack(pady=10)

chat_box = tk.Text(root, height=20, width=60,
                   bg="#ffffff", fg="#2c3e50",
                   font=("Helvetica", 10),
                   relief=tk.GROOVE, bd=2)
chat_box.pack(padx=10)

input_frame = tk.Frame(root, bg="#f0f4f8")
input_frame.pack(pady=8)

entry = tk.Entry(input_frame, width=38, font=("Helvetica", 10))
entry.pack(side=tk.LEFT, padx=5)

tk.Button(input_frame, text="Send 💬",
          command=send_message,
          bg="#2ecc71", fg="white",
          font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)

root.mainloop()