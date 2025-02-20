# Use the official Python image
FROM python:3.9
# Set the working directory inside the container
WORKDIR /app

# Copy the required files into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY weather_alert.py .
RUN mkdir -p /app/data

# Set the environment variable for the API key (Replace with your actual key or set it at runtime)
ENV WEATHER_API_KEY="5205abee21d0a9848c3187a8c385942f"

# Run the script
CMD ["python", "-u", "/app/weather_alert.py"]
