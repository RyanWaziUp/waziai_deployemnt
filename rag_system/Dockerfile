FROM python:3.12.5-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

COPY db /app/db

COPY embedding_model /app/embedding_model

COPY src /app/src

COPY main.py /app/main.py

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir sentence-transformers

EXPOSE 8080


HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "main.py"]