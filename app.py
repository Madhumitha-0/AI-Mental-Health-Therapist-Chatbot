import tkinter as tk
from textblob import TextBlob
import random

# Create window
root = tk.Tk()
root.title("AI Mental Health Therapist")
root.geometry("550x650")

bot_name = "AI Mental Health Therapist"

# Chat display
chat_area = tk.Text(root, wrap=tk.WORD)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, width=65)
entry.pack(padx=10, pady=10)

# Conversation state variables
step = 0
name = ""
gender = ""
age = 0
age_group = ""

chat_area.insert(tk.END, f"{bot_name}: Hi 👋 I am {bot_name}.\n")
chat_area.insert(tk.END, f"{bot_name}: What is your name?\n\n")

# Emotion Detection
def detect_emotion(message):
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity

    if polarity > 0.4:
        return "happy"
    elif polarity < -0.4:
        return "sad"
    elif "angry" in message.lower():
        return "anger"
    elif "fear" in message.lower() or "scared" in message.lower():
        return "fear"
    else:
        return "neutral"

# Response Generator
def generate_response(emotion, age_group, name):

    if emotion == "happy":
        return f"That’s wonderful to hear, {name}! 😊 I'm really glad you're feeling happy. If you ever need support or someone to talk to, I’m always here for you. Take care and keep smiling 🌸"

    elif emotion == "sad":
        if age_group == "Teen":
            return f"I'm sorry you're feeling sad, {name}. 💙 It’s okay to feel this way. Try talking to someone you trust and do something you enjoy. Remember, this phase will pass."
        elif age_group == "Adult":
            return f"I understand, {name}. 🤍 When feeling sad, try taking a short walk, practice deep breathing, or speak with a close friend. Small steps can slowly improve your mood."
        else:
            return f"{name}, sadness can feel heavy. 💛 Try relaxing activities like listening to calm music, light exercise, or sharing your thoughts with loved ones."

    elif emotion == "anger":
        return f"I can sense you're feeling angry, {name}. 😌 Take 5 slow deep breaths. Step away from the situation for a few minutes. Responding calmly will help you feel more in control."

    elif emotion == "fear":
        return f"It's okay to feel scared sometimes, {name}. 💪 Try grounding yourself — focus on your breathing and remind yourself that you are safe. You are stronger than you think."

    else:
        return f"I’m here for you, {name}. ❤️ Can you tell me a little more about how you're feeling?"
def send_message():
    global step, name, gender, age, age_group

    user_message = entry.get()
    chat_area.insert(tk.END, f"You: {user_message}\n")
    entry.delete(0, tk.END)

    if step == 0:
        name = user_message
        chat_area.insert(tk.END, f"{bot_name}: Nice to meet you, {name}! 😊\n")
        chat_area.insert(tk.END, f"{bot_name}: What is your gender?\n\n")
        step = 1

    elif step == 1:
        gender = user_message
        chat_area.insert(tk.END, f"{bot_name}: Thank you.\n")
        chat_area.insert(tk.END, f"{bot_name}: What is your age?\n\n")
        step = 2

    elif step == 2:
        try:
            age = int(user_message)
            if age < 18:
                age_group = "Teen"
            elif age < 40:
                age_group = "Adult"
            else:
                age_group = "Senior"

            chat_area.insert(tk.END, f"{bot_name}: Got it 👍\n")
            chat_area.insert(tk.END, f"{bot_name}: How are you feeling today?\n\n")
            step = 3
        except:
            chat_area.insert(tk.END, f"{bot_name}: Please enter a valid age number.\n\n")

    else:
        emotion = detect_emotion(user_message)
        reply = generate_response(emotion, age_group,name)

        chat_area.insert(tk.END, f"{bot_name}: (Detected emotion: {emotion})\n")
        chat_area.insert(tk.END, f"{bot_name}: {reply}\n\n")

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)
root.mainloop()