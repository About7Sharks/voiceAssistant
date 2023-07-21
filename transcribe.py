import sys
import whisper


def main():
    # sys.argv is a list in Python, which contains the command-line arguments passed to the script.
    # With the help of this, you can accept a filename when running the script from the command line
    filename = sys.argv[1]

    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print(result["text"])

if __name__ == "__main__":
    main()
