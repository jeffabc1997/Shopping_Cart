FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Expose the port
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]