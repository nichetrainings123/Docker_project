# Python Base Image
FROM python:3.10-slim

# Working Directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Flask Environment Variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose Flask Port
EXPOSE 5000

# Run Flask Application
CMD ["python", "app.py"]