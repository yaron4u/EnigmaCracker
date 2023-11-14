# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Run the script when the container launches
CMD ["python", "./EC.py"]
