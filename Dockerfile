# Use a base image that has Python
FROM python:3.11-slim

# Install MySQL development libraries
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your application code
COPY . /app

# Set the working directory
WORKDIR /app

# Command to run your app
CMD ["python3", "-m","api.v2.app"]  # Replace with your app's entry point
