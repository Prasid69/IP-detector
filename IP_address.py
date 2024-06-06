import requests #here, it sends http requests

def get_ip():
    response = requests.get('https://api64.ipify.org/?format=json').json()
    return response["ip"]

def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

def check_vpn(ip_address, api_key):
    url = f"https://vpnapi.io/api/{ip_address}?key={api_key}"
    response = requests.get(url)
    vpn_data = response.json()
    return vpn_data

def main():
    api_key = 'cc1f480e5aa34bdb9119e243b46f9146'
    user_ip = input("Enter an IP address (or press Enter to use your own IP): ")
    if not user_ip:
        user_ip = get_ip()
    
    vpn_info = check_vpn(user_ip, api_key)
    print("\nVPN/Proxy Detection Info:")
    print(vpn_info)
    
    location = get_location(user_ip)
    print("\nGeolocation Info:")
    print(location)

if __name__ == "__main__":
    main()



