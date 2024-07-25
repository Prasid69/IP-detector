FROM python:3.12.3
WORKDIR /IP_address

COPY . /IP_address

# Install any needed packages 
RUN pip install dnspython geoip2

CMD ["python3", "IP_address.py"]


