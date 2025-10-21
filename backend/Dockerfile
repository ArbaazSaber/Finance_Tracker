## Base image: use an official slim Python image to keep size small
FROM python:3.11-slim

## Ensure Python output is sent straight to the container logs (no buffering)
ENV PYTHONUNBUFFERED=1

## Set the working directory inside the container
WORKDIR /app

## Copy only the requirements first to leverage Docker layer caching.
## When requirements.txt doesn't change, Docker will reuse this layer and skip reinstalling packages.
COPY requirements.txt ./

## Install Python dependencies. --no-cache-dir prevents pip from caching packages in the image.
RUN pip install --no-cache-dir -r requirements.txt

## Copy application source code into the image. Placing this after dependency installation
## means code changes won't invalidate the dependency layer.
COPY . /app

## Expose the port the application will run on. This is informational for users and tooling.
EXPOSE 8000

## Default command: start the FastAPI app with Uvicorn on all interfaces so it is reachable from the host
## Do not use --reload in production since it watches files and is intended for development.
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

ENTRYPOINT [ "python" , "/app/app.py" ]