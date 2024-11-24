from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import sqlite3
import cv2
import speech_recognition as sr
import numpy as np
from io import BytesIO

app = FastAPI()

# Database setup
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        face_encoding BLOB,
        audio_encoding BLOB
    )
""")
conn.commit()

# Helper functions for face detection and audio recognition

def get_face_encoding(image_bytes):
    # Use OpenCV or any other model to extract face encoding
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    # Here you would use a facial recognition model to get the encoding, e.g., dlib, or FaceNet
    return np.random.random(128)  # Placeholder for the face encoding

def get_audio_encoding(audio_bytes):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(BytesIO(audio_bytes))
    with audio as source:
        audio_data = recognizer.record(source)
    # Use SpeechRecognition to process the audio and return its encoding
    return recognizer.recognize_google(audio_data)  # Placeholder for the audio encoding

# Pydantic model for user sign-up

class User(BaseModel):
    email: str

@app.post("/signup")
async def signup(user: User, file: UploadFile = File(...), audio: UploadFile = File(...)):
    face_data = await file.read()
    audio_data = await audio.read()

    face_encoding = get_face_encoding(face_data)
    audio_encoding = get_audio_encoding(audio_data)

    cursor.execute("INSERT INTO users (email, face_encoding, audio_encoding) VALUES (?, ?, ?)",
                   (user.email, face_encoding.tobytes(), audio_encoding))
    conn.commit()

    return {"message": "User signed up successfully!"}

@app.post("/login")
async def login(user: User, file: UploadFile = File(...), audio: UploadFile = File(...)):
    face_data = await file.read()
    audio_data = await audio.read()

    face_encoding = get_face_encoding(face_data)
    audio_encoding = get_audio_encoding(audio_data)

    cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
    stored_user = cursor.fetchone()

    if stored_user:
        stored_face_encoding = np.frombuffer(stored_user[1], np.float64)  # Example decoding from BLOB
        stored_audio_encoding = stored_user[2]

        # Match face and audio encoding (this would involve actual comparison algorithms)
        if np.allclose(face_encoding, stored_face_encoding) and audio_encoding == stored_audio_encoding:
            return {"message": "Login successful!"}
        else:
            return {"message": "Face or audio does not match!"}
    else:
        return {"message": "User not found!"}

# Run the app with uvicorn
# uvicorn main:app --reload