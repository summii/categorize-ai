# Use the official Python image
FROM python:3.11-slim-buster

# Set the working directory in the container
# Set the working directory
WORKDIR /categorize-ai



# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Add the current directory to PYTHONPATH
ENV PYTHONPATH=/categorize-ai:$PYTHONPATH

# Expose the port the app runs on
EXPOSE 8000

# Run the application (replace `app.py` with your main script)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]