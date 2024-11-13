# Use the official Python image
FROM python:3.8.7

# Set the working directory in the container
WORKDIR /.

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the application (replace `app.py` with your main script)
CMD ["python", "main.py"]