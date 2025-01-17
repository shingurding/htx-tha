"""
cv-decode.py

This script is used to call the API from `asr_api.py` to transcribe the 4,076 common-voice mp3 files under `cv-valid-dev` folder.
"""
import os
import requests
import pandas as pd
from tqdm import tqdm

def get_transcription(audio_filepath):
    """
    Sends a POST request to the ASR API to get the transcription.
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