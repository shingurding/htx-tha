"""
cv-decode.py

This script interacts with the ASR API provided by the `asr_api.py` script to transcribe a collection of mp3 audio files located in `common_voice/cv-valid-dev` folder of the Common Voice dataset.
The transcriptions are generated for the 4,076 audio files and saved in a new CSV file (`cv-valid-dev-generated.csv`).

The script does the following:
1. Reads the CSV file (`common_voice/cv-valid-dev.csv`) to get the metadata of the audio files.
2. For each audio file, it sends a POST request to the ASR API to get the transcription.
3. The CSV file (`cv-valid-dev-generated.csv`) is updated with the transcriptions.
"""
import os
import requests
import pandas as pd
from tqdm import tqdm

def get_transcription(audio_filepath):
    """
    Sends a POST request to the ASR API to get the transcription for the given audio.

    Args:
        audio_filepath (str): The path to the audio file that needs to be transcribed.

    Returns:
        str: The transcription text returned by the ASR API.
    """
    with open(audio_filepath, 'rb') as f:
        files = {
            "file": f
        }
        response = requests.post(url="http://localhost:8001/asr", files=files)
        
        if response.status_code == 200:
            transcription = response.json().get('transcription', '')
            return transcription
        else:
            print(f"error for {audio_filepath}: {response.text}")
            return None


def main():
    """
    The main function to load the audio file metadata, send requests to the ASR API for transcription,
    and update the CSV file with the transcriptions.
    """
    audio_path = os.path.join("asr", "common_voice", "cv-valid-dev")
    
    # Read cv_valid_dev csv file
    cv_valid_dev_df = pd.read_csv("asr/common_voice/cv-valid-dev.csv")[2739:]

    # Iterate through each row in the csv file to get the audio transcription
    for idx, row in tqdm(cv_valid_dev_df.iterrows(), total=cv_valid_dev_df.shape[0], desc="Transcribing audios..."):
        audio_filename = row["filename"]
        audio_filepath = os.path.join(audio_path, audio_filename)

        # Get transcription
        transcription = get_transcription(audio_filepath)

        # Update generated_text column for the current row
        cv_valid_dev_df.loc[idx, "generated_text"] = transcription

        # Save the updated file into the same file
        cv_valid_dev_df.iloc[:idx+1].to_csv("asr/common_voice/cv-valid-dev-generated.csv", index=False)
        
    print("Updated file successfully saved!")


if __name__ == '__main__':
    main()