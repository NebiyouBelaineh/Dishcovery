# Setup base image from Offical Python runtime
FROM python:3.10-slim

# Install System level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Define environment variables, sensitive data such as passwords\
# should be used during runtime
ENV DISHCOVERY_MYSQL_USER=dishcovery_dev
ENV DISHCOVERY_MYSQL_PWD=dishcovery_dev_pwd
ENV DISHCOVERY_MYSQL_HOST=localhost
ENV DISHCOVERY_MYSQL_DB=dishcovery_dev_db
ENV DISHCOVERY_ENV=db
# # Need to load all from .env file
# ENV DISHCOVERY_SECRET_KEY=secret
# ENV API_KEY=api_key
# ENV API_ID=api_id

# Expose the Application Port
EXPOSE 5000

# Run the App
CMD ["python3", "app.py"]

