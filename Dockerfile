FROM python:3.11-slim

WORKDIR /app

# System deps (Pillow can require freetype/jpeg libs; keep minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# App source
COPY src /app/src
COPY streamlit_app.py /app/streamlit_app.py

# Model artifact (expected by src/streamlit_app/pages/predict.py)
# Put model.pkl at repo root.
COPY model.pkl /app/model.pkl

EXPOSE 8501

ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501

CMD ["streamlit", "run", "/app/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]

