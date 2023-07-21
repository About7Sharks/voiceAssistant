import multiprocessing
import queue
import time
import pyaudio
import wave
import sqlite3
from sqlite3 import Error
import subprocess
import os
import warnings

warnings.filterwarnings("ignore")

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

def record_audio(filename_queue):
    chunk = 1024  
    sample_format = pyaudio.paInt16  
    channels = 1
    fs = 44100  
    seconds = 5
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

        print('Finished recording')

        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        filename_queue.put(filename)
        # time.sleep(seconds)

def transcribe_audio(filename_queue):
    conn = create_connection()
    create_table(conn)
    while True:
        if not filename_queue.empty():
            filename = filename_queue.get()
            print(filename)
            result = subprocess.check_output(['python3', 'transcribe.py', filename])
            insert_transcription(conn, result.decode('utf-8'))

def transcribe_audio(filename_queue):
    conn = create_connection()
    create_table(conn)
    while True:
        if not filename_queue.empty():
            filename = filename_queue.get()
            print(filename)
            result = subprocess.check_output(['python3', 'transcribe.py', filename])
            insert_transcription(conn, result.decode('utf-8'))
            os.remove(filename)  # Delete the file after transcribing

if __name__ == "__main__":
    # Create a Manager object to manage the shared state
    manager = multiprocessing.Manager()

    # Create a Queue object through the manager
    filename_queue = manager.Queue()

    # Create two processes
    recorder_process = multiprocessing.Process(target=record_audio, args=(filename_queue,))
    transcriber_process = multiprocessing.Process(target=transcribe_audio, args=(filename_queue,))

    # Start the processes
    recorder_process.start()
    transcriber_process.start()

    # Wait for the processes to finish
    recorder_process.join()
    transcriber_process.join()