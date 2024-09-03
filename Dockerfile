# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file into the container at /app
COPY requirements.txt .

# Step 3.5: Install tesseract OCR
RUN apt-get update && apt install tesseract-ocr -y

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code to the container
COPY . /app

# Step 6: Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Step 7: Command to run the Flask app
CMD ["python", "app.py"]