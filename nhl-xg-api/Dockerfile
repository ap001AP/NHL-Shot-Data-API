FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libgomp1 wget curl unzip && \
    ARCH=$(dpkg --print-architecture) && \
    wget https://github.com/grafana/alloy/releases/download/v1.3.1/alloy-linux-${ARCH}.zip && \
    unzip alloy-linux-${ARCH}.zip && \
    mv alloy-linux-${ARCH} /usr/local/bin/alloy && \
    chmod +x /usr/local/bin/alloy && \
    rm alloy-linux-${ARCH}.zip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY model/ ./model/
COPY alloy-config.alloy .
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]