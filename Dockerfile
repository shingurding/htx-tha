FROM python:3.10-slim

# Set the working directory within the container
WORKDIR /app

# Download ffmpeg to process audio
RUN apt-get update && \
    apt-get install -y ffmpeg libsndfile1 curl && \
    rm -rf /var/lib/apt/lists/*

# Copy the asr_api.py script
COPY asr/asr_api.py /app/asr/asr_api.py

# Copy requirements.txt
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create temporary dir for processing
RUN mkdir -p /app/asr/tmp

# Export port
EXPOSE 8001

# Run the asr_api.py script
CMD ["python", "/app/asr/asr_api.py"]