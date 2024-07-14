import requests

def call_ip_check_api(ip_address):
    url = f"http://127.0.0.1:5000/check_ip?ip={ip_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to retrieve data', 'status_code': response.status_code}

if __name__ == "__main__":
    ip_address = '178.20.55.182'
    result = call_ip_check_api(ip_address)
    print(result)
