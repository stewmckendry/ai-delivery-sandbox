FROM python:3.11-slim

WORKDIR /app
COPY . .

<<<<<<< 50qpub-codex/create-railway-deployment-guide-for-fastapi
RUN apt-get update && apt-get install -y build-essential unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

=======
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> sandbox-curious-fox
