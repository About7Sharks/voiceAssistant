# Voice Transcription App

This is a voice transcription app that records audio, transcribes it using the Whisper ASR (Automatic Speech Recognition) model, and stores the transcriptions in a SQLite database. The application is built with Python, using the PyAudio library for recording audio, the Whisper ASR model for transcribing the audio, and SQLite for storing the transcriptions.

## Features

- **Continuous Audio Recording:** The app continuously records audio in 30-second intervals, saving each recording as a separate `.wav` file.
- **Real-time Transcription:** After each recording, the app transcribes the audio using the Whisper ASR model.
- **Database Storage:** The transcriptions are stored in a SQLite database, along with a timestamp and a unique ID for each transcription.
- **Concurrent Processing:** The app uses Python's threading capabilities to record and transcribe audio concurrently, ensuring that no audio is lost between transcriptions.

## Installation

1. Clone this repository.

2. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```

3. Download the Whisper ASR model:

    ```
    wget https://example.com/whisper/model
    ```

   Replace `https://example.com/whisper/model` with the actual URL of the Whisper ASR model.

## Usage

To start the app, run the `server.py` script:

```
python server.py
```

The app will start recording audio and transcribing it in real time. The transcriptions will be stored in a SQLite database named `transcriptions.db`.

## Future Improvements

- **Frontend Dashboard:** A frontend dashboard could be added to visualize the transcriptions in real time. This dashboard could use a modern frontend framework like React or Vue.js, and it could fetch the transcriptions from the SQLite database using a REST API.

- **Sentiment Analysis:** The transcriptions could be analyzed for sentiment using a sentiment analysis API or library. This could provide insights into the tone of the spoken text.

- **Speech-to-Text API:** The Whisper ASR model could be replaced with a speech-to-text API for potentially more accurate transcriptions. This would require modifications to the `transcribe.py` script.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.
