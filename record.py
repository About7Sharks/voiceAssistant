import threading
import queue
import time
import pyaudio
import wave
import sqlite3
from sqlite3 import Error
import subprocess

# Create a queue to hold the filenames of the audio files to be transcribed
filename_queue = queue.Queue()

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('transcriptions.db') 
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(f'Error occurred: {e}')
    return conn

def create_table(conn):
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Speech(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                transcription TEXT NOT NULL);
        """)
        print('table created successfully')
    except Error as e:
        print(f'Error occurred: {e}')

def insert_transcription(conn, transcription):
    try:
        conn.execute("""
            INSERT INTO Speech(transcription)
            VALUES(?);
        """, (transcription,))
        conn.commit()
        print('transcription inserted successfully')
    except Error as e:
        print(f'Error occurred: {e}')

def record_audio():
    chunk = 1024  
    sample_format = pyaudio.paInt16  
    channels = 1
    fs = 44100  
    seconds = 15
    p = pyaudio.PyAudio()  

    while True:
        filename = f"output{int(time.time())}.wav"
        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []

        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        #stream.close()
        #p.terminate()

        print('Finished recording')

        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        filename_queue.put(filename)
        time.sleep(seconds)  # record every 3 seconds

def transcribe_audio():
    conn = create_connection()
    create_table(conn)
    while True:
        if not filename_queue.empty():
            filename = filename_queue.get()
            # Pass the filename to your transcription script
            print(filename)
            result = subprocess.check_output(['python3', 'transcribe.py', filename])
            insert_transcription(conn, result.decode('utf-8'))


def main():
    # Create two threads
    recorder_thread = threading.Thread(target=record_audio)
    transcriber_thread = threading.Thread(target=transcribe_audio)

    # Start the threads
    recorder_thread.start()
    transcriber_thread.start()

    # Wait for the threads to finish (they won't, because they're infinite loops)
    recorder_thread.join()
    transcriber_thread.join()

if __name__ == "__main__":
    main()
