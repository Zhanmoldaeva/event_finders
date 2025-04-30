from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from openai import OpenAI
import pyttsx3

app = Flask(__name__)

client = OpenAI(api_key='your-api-key')
recognizer = sr.Recognizer()
engine = pyttsx3.init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    audio_file = request.files['audio']
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='ru-RU')
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный помощник, отвечай на русском языке."},
                {"role": "user", "content": text}
            ]
        ).choices[0].message.content
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)