FROM python:3.10-slim

# Install curl, zstd, and system dependencies required by Ollama installer
RUN apt-get update && apt-get install -y curl zstd && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

# Copy requirements & install python dependencies
COPY Backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend code
COPY Backend /app/Backend

# Hugging Face Spaces exposes port 7860
EXPOSE 7860

CMD ["sh", "-c", "ollama serve & sleep 2 && (ollama pull phi3 &) && uvicorn Backend.app:app --host 0.0.0.0 --port ${PORT:-7860}"]

