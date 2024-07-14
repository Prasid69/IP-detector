FROM python:3.12.3
WORKDIR /IP_address
# Copy the current directory contents into the container at /IP_address
COPY . /IP_address

# Install any needed packages 
RUN pip install dnspython geoip2

# Run the command to start the script
CMD ["python3", "IP_address.py"]


