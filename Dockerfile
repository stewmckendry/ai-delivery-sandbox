FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg2 apt-transport-https unixodbc-dev libodbc2 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean

# Set working directory
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port and run
EXPOSE 8000
CMD uvicorn app.main:app --host=0.0.0.0 --port=8000