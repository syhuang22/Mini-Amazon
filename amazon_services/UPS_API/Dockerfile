FROM python:3.8-slim-buster
COPY . /UPS_API
WORKDIR /UPS_API

# Install the external dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 6543 for incoming connections
EXPOSE 6543

# Run main.py when the container launches
CMD ["python3", "main.py"]