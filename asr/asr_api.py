"""
asr_api.py

Creates a Flask App for the API.
"""
import os
import torch
import numpy as np

from flask import Flask, jsonify, request
from pydub import AudioSegment
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


# Initialise Flask app
app = Flask(__name__)
app.config["DEBUG"] = True

# Create a temporary dir to save the audio file
TEMP_DIR = "./asr/tmp/"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/ping', methods=['GET'])
def ping():
    """
    An endpoint to check if the service is working.
    """
    return jsonify({
        "response": "pong"
    })

@app.route('/asr', methods=['POST'])
def asr():
    """
    An endpoint to transcribe an audio.

    Returns:
        transcription (str): The transcribed text returned by the model.
        duration (str): The duration of the file in seconds.
    """
    try:
        # Read the audio file into the temp dir
        f = request.files['file']
        file_path = os.path.join(TEMP_DIR, f.filename)
        f.save(file_path)

        audio = AudioSegment.from_file(file_path, format="mp3")

        # Get duration of the audio in seconds
        duration = len(audio) / 1000 
        duration_str = str(duration)

        # Convert audio to appropriate fornat
        audio = audio.set_channels(1).set_frame_rate(16000)  # Convert to 16kHz
        audio_arr = np.array(audio.get_array_of_samples())

        # Load pretrained model from huggingface
        processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

        # Tokenize
        input_values = processor(audio_arr, return_tensors="pt", padding="longest").input_values
        input_values = input_values.to(torch.float32)  # Convert to float32 tensor

        # Retrieve logits
        logits = model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    
    finally:
        # Delete audio once it's done processing
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify({
        "transcription": transcription[0],
        "duration": duration_str
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001)