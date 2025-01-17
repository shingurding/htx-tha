FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /app

# Download ffmpeg to process audio
RUN apt-get update && \
    apt-get install -y ffmpeg libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

# Copy all the contents into the /app dir in the container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create temporary dir
RUN mkdir -p /app/asr/tmp

# Export port
EXPOSE 8001

# Run the asr_api.py script
CMD ["python", "asr/asr_api.py"]