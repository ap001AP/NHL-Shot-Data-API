FROM python:3.11-slim

WORKDIR /app

# Install system dependencies + Alloy
RUN apt-get update && \
    apt-get install -y libgomp1 wget curl && \
    wget https://github.com/grafana/alloy/releases/download/v1.3.1/alloy-linux-amd64.zip && \
    apt-get install -y unzip && \
    unzip alloy-linux-amd64.zip && \
    mv alloy-linux-amd64 /usr/local/bin/alloy && \
    chmod +x /usr/local/bin/alloy && \
    rm alloy-linux-amd64.zip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY model/ ./model/
COPY alloy-config.alloy .

# Start script to run both API and Alloy
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]