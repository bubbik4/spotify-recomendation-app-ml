FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git git-lfs ca-certificates && rm -rf /var/lib/apt/lists/*
RUN git lfs install

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG GITHUB_TOKEN

RUN git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/" && \
    git lfs pull && \
    git config --global --remove-section url."https://${GITHUB_TOKEN}@github.com/"

EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
