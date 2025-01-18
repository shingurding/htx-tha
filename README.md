# HTX Take-Home-Assessment

## Indtroduction

This repository contains the code for the following:

1. Hosting a microservice to deploy Automatic Speech Recognition (ASI) AI model that can be used to transcribe any audio files.
2. Code for fine-tuning an ASR AI model.
3. Code for detecting hotwords in audio.
4. A training report for comparing the pre-trained ASR AI model and fine-tuned ASR AI model.
5. An essay proposing a model self-supervised learnig pipeline to cater dysarthric speech.

## Getting Started

1. Clone this repository:

    ```bash
    git clone https://github.com/shingurding/htx-tha.git

    # Navigate into the repository
    cd htx-tha
    ```

2. Create a virtual environment:
   
    ```bash
    python3 -m venv .venv

    # Activate the environment
    source .venv/bin/activate  # On macOS / Linux

    .\.venv\Scripts\Activate  # On Windows (PowerShell)
    ```

3. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Add the required dataset to the corresponding `common_voice` folders under `asr/common_voice/`, `asr-train/common_voice/`, and `hotword-detection/common_voice/` (see [Repository Structure](#repository-structure)).

## Usage

### Running ASR Microservice

1. To run the microservice directly (local python), run the following line:

    ```bash
    python asr/asr_api.py
    ```
    This launches the ASR API, running on port `8001` (or as configured in the script).

2. Using Docker:

    ```bash
    docker build -t asr-api .
    docker run -p 8001:8001 asr-api
    ```
    The microservice is then accessible on `http://localhost:8001`.

## Repository Structure

```
/htx-tha
├── .gitignore
├── requirements.txt
├── README.md
├── Dockerfile                         # Task 2e
├── training-report.pdf                # Training report for comparison of models (task 4)
├── essay-ssl.pdf                      # Self-supervised learning essay (task 6)
├── asr/                               # Directory for ASR API microservice
│   ├── asr_api.py                     # Task 2b, 2c
│   ├── cv-decode.py                   # Task 2d
│   ├── cv-valid-dev-generated.csv     # Dataset with `generated_text` column (task 2d)
│   └── common_voice/                  # Directory containing the dataset (to be added)
│       ├── cv-valid-dev.csv
│       └── cv-valid-dev/ 
├── asr-train/                         # Directory for fine-tuning the ASR model
│   ├── cv-train-2a.ipynb              # Jupyter notebook for fine-tuning ASR model (task 3)
│   ├── common_voice/                  # Directory containing the dataset for training (to be added)
│   │   ├── cv-valid-train.csv
│   │   ├── cv-valid-test.csv
│   │   ├── cv-valid-train/
│   │   └── cv-valid-test/
│   ├── cv-valid-test-result.csv       # Updated dataset that contains the generated text using the fine-tuned model on `cv-valid-test.csv`
│   └── wav2vec2-large-960h-cv/
│       └── ...                        # Fine-tuned model weights
├── hotword-detection/                 # Directory for hotword detection task (task 5)
│   ├── cv-hotword-5a.ipynb            # Jupyter notebook for detecting hotwords
│   ├── cv-hotword-similarity-5b.ipynb # Jupyter notebook for hotword similarity detection
│   ├── detected.txt                   # Task 5a
│   ├── cv-valid-dev                   # Original cv-valid-sev dataset
│   ├── cv-valid-dev-ft-generated.csv  # Dataset with the fine-tuned model generated text column (task 4)
│   └── cv-valid-dev-similarity.csv    # Dataset with `similarity` column (task 5b)
```