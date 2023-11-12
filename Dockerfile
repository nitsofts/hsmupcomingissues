# Use an official Selenium base image with ChromeDriver
FROM selenium/standalone-chrome:latest

# Set the working directory
WORKDIR /usr/src/app

# Copy the local code to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]
