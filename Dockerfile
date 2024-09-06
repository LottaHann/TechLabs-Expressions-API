# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set the working directory in the container

WORKDIR /app

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container at /app

COPY . .
ARG SERVER_URL=http://server:8008

# Set environment variable from build argument
ENV SERVER_URL=$SERVER_URL

# Make port 80 available to the world outside this container
# Adjust this if your application uses a different port
EXPOSE 5000
EXPOSE 5500


# Run app.py when the container launches
CMD ["python", "app/main.py"]