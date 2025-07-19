import os
import sqlite3
import pyttsx3
import time
from datetime import datetime
print("Current working directory:", os.getcwd())

    # Now you can directly use the 'date' object, e.g., today = date.today()

# Initialize voice
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# === Memory Setup ===
def init_memory():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    content TEXT
                )''')
    conn.commit()
    conn.close()

# === Voice Assistant ===
def speak(text):
    print(f"Raphale: {text}")
    engine.say(text)
    engine.runAndWait()

# === Learn from File ===
def learn_from_file(file_path="lessons.txt"):
    if not os.path.exists(file_path):
        speak("No lesson file found.")
        return

    conn = sqlite3.connect("memory.db")
    c = conn.cursor()

    lesson_path = os.path.join(os.path.dirname(__file__), "lessons.txt")
    with open(lesson_path, "r") as file:
        for line in file:
            if "::" in line:
                topic, content = line.strip().split("::", 1)
                c.execute("INSERT INTO knowledge (topic, content) VALUES (?, ?)", (topic, content))
                log_thought(f"Learned: {topic} → {content}")
                speak(f"I have learned about {topic}.")
    conn.commit()
    conn.close()
if __name__ == "__main__":
    lesson_path = input("📥 Enter full path to lesson file: ")
    load_lessons(lesson_path)

# === Thought Logging ===
def log_thought(text):
    with open("thoughts.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {text}\n")

# === Recall ===
def recall(topic):
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("SELECT content FROM knowledge WHERE topic LIKE ?", (f"%{topic}%",))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "I don't remember anything about that."
  
# === Process Input ===
def process_input(user_input):
    if user_input.lower().startswith("learn"):
        learn_from_file()
    elif user_input.lower().startswith("recall"):
        topic = user_input.split(" ", 1)[-1]
        memory = recall(topic)
        speak(memory)
    elif user_input.lower().startswith("think"):
        speak("Let me think about that...")
        log_thought(f"Thinking about: {user_input}")
        speak("I have noted the thought.")
    elif user_input.lower().startswith("shutdown"):
        speak("Goodbye.")
        exit()
    else:
        speak("I do not understand yet, but I will learn.")
        log_thought(f"Unknown command: {user_input}")
        
# === Start ===
if __name__ == "__main__":
    

    speak("Initializing Raphale v2.")
    init_memory()
    learn_from_file()
   
    while True:
        user_input = input("You: ")
        process_input(user_input)
    
