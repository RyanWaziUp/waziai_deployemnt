FROM python:3.12.5-slim

WORKDIR /app

COPY main.py /app/main.py

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "main.py"]