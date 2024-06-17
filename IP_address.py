import requests

def get_ip():
    response = requests.get('https://api64.ipify.org/?format=json').json()
    return response["ip"]

def get_location(ip_address, api_key):
    response = requests.get(f'https://ipinfo.io/{ip_address}?token={api_key}').json()
    location_data = {
        "ip": ip_address,
        "City Name": response.get('city'),
        "Region": response.get('region'),
        "Country": response.get('country'),
        "Time Zone": response.get('timezone')    
    }
    return location_data

def for_vpn_proxy(ip_address, api_key):
    response = requests.get(f'https://vpnapi.io/api/{ip_address}?key={api_key}').json()
    vpn_proxy = {
        "ip": ip_address,
        "VPN": response.get('security', {}).get('vpn'),
        "Proxy": response.get('security', {}).get('proxy'),
        "Tor": response.get('security', {}).get('tor')
    }
    return vpn_proxy

def main():
    ipinfo_api_key = 'a68557753f2cbd'  
    vpnapi_api_key = 'cc1f480e5aa34bdb9119e243b46f9146'  
    
    user_ip = input("Enter an IP address (or press Enter to use your own IP): ") #current ko ip
    if not user_ip:
        user_ip = get_ip()

    current_location = get_location(user_ip, ipinfo_api_key)
    vpn_proxy_info = for_vpn_proxy(user_ip, vpnapi_api_key)
   
    previous_ip = input("Enter a previous IP address (or press Enter if not available): ") #previous ko
    previous_country = None

    if previous_ip:
        previous_location = get_location(previous_ip, ipinfo_api_key)
        previous_country = previous_location["Country"]

    print("Geolocation Info:")
    print(current_location)
    
    print("VPN and Proxy Info:")
    print(vpn_proxy_info)
    if vpn_proxy_info["VPN"]:
        print("The IP address is using a VPN.")
    if vpn_proxy_info["Proxy"]:
        print("The IP address is using a Proxy.")
    if vpn_proxy_info["Tor"]:
        print("The IP address is using Tor.")
    
    if previous_country != current_location["Country"]:
        print(f"The country has changed from {previous_country} to {current_location['Country']}.")
    else:
        print("The country has not changed.")

if __name__ == "__main__":
    main()



