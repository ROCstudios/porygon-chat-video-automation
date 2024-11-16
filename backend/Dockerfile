# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for the port
ENV PORT 8080

# Expose the port
EXPOSE 8080

# Run main.py when the container launches
CMD ["python", "init.py"]
