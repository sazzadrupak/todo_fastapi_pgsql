# Use the official Python image from the Docker Hub
FROM python:3.12.7-alpine
LABEL maintainer="sazzad.rupak"

# Set environment variables

##  Prevents Python from writing .pyc files to disk
# ENV PYTHONDONTWRITEBYTECODE=1
## Ensures Python output is printed to the terminal (stdout and stderr)
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app

ARG DEV=false
# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        fastapi-user

ENV PATH="/py/bin:$PATH"


# Copy the rest of the application code

USER fastapi-user

# Expose the FastAPI app's default port
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]