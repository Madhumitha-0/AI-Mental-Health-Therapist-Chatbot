🤖 AI Mood Detection Chatbot (Desktop App)

📌 Project Overview

The AI Mood Detection Chatbot is a desktop-based application that detects a user's facial expression using a webcam and responds with appropriate chatbot messages based on the detected emotion.

This project combines Computer Vision + AI + GUI to create an interactive mental health support assistant.

---

🎯 Objectives

- Detect human face using webcam
- Analyze facial expressions to determine mood
- Provide chatbot responses based on user mood
- Create a user-friendly desktop application

---

✨ Features

- 📷 Real-time face detection using camera
- 🧠 Emotion detection using AI (FER library)
- 👤 User input (Name, Age, Gender)
- 💬 Interactive chatbot interface
- 😊 Mood-based responses (Happy, Sad, Angry, Neutral)
- 🔁 Continuous chat until user exits

---

🛠️ Technologies Used

- Python 3.14
- OpenCV – for face detection
- FER (Facial Emotion Recognition) – for emotion detection
- TensorFlow – backend support for FER
- Tkinter – for GUI (desktop application)

---

⚙️ Installation & Setup

Step 1: Clone the Repository

git clone https://github.com/Madhumitha-0/AI-Mental-Health-Chatbot.git
cd ai-mood-chatbot

---

Step 2: Install Required Libraries

pip install opencv-python fer tensorflow

---

Step 3: Run the Application

python main.py

---

📂 Project Structure

ai-mood-chatbot/
│
├── main.py              # Main application file
├── README.md            # Project documentation
├── requirements.txt     # Dependencies (optional)

---

🧠 How It Works

1. User enters name, age, and gender
2. Camera starts and detects face
3. Emotion is analyzed using AI model
4. Mood is displayed (Happy/Sad/Angry/Neutral)
5. Chatbot starts conversation
6. Bot gives responses based on:
   - User input
   - Detected mood
7. Chat continues until user types "bye"

---

📸 Output Screens

- Camera window for face detection
- GUI chatbot window
- Mood displayed on screen
- Interactive chat messages

---

⚠️ Limitations

- Emotion detection may not be 100% accurate
- Requires proper lighting for better results
- Needs webcam access

---

🚀 Future Enhancements

- Voice input and output
- More accurate deep learning model
- Mobile app version
- Database to store chat history

---

👩‍💻 Author

Name: Madhumitha.V

---

📜 License

This project is for educational purposes only.
