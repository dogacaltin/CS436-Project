FROM python:3.11-slim

WORKDIR /app

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/thermal-imprint-459211-c7-0f9c10fab178.json"

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
