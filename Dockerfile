FROM python:3.12-slim as lfs-builder

RUN apt-get update && apt-get install -y git git-lfs ca-certificates && rm -rf /var/lib/apt/lists/*
RUN git lfs install

ARG GITHUB_TOKEN

RUN if [ -n "$GITHUB_TOKEN" ]; then \
        git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"; \
    fi && \
    git clone --depth 1 https://github.com/bubbik4/spotify-recomendation-app-ml.git /tmp/repo

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=lfs-builder /tmp/repo/data/* /app/data/

EXPOSE 8501

# Komenda startowa
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
