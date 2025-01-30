# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Expose the Flask port
EXPOSE 5000

# Set environment variables (Optional: If you need it)
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]