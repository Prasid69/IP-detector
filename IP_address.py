import geoip2.database
import ipaddress
import dns.resolver

def load_vpn_ip_list(file_path):
    with open(file_path, 'r') as file:
        vpn_ips = file.read().splitlines()
    return vpn_ips

def is_ip_in_vpn_list(ip_address, vpn_ips):
    ip = ipaddress.ip_address(ip_address)
    for vpn_ip in vpn_ips:
        if '/' in vpn_ip:  # Handle IP ranges
            if ip in ipaddress.ip_network(vpn_ip):
                return True
        else:
            if ip_address == vpn_ip:
                return True
    return False

def check_vpn_using_geolocation(ip_address):
    reader = geoip2.database.Reader('./db/GeoLite2-City_20240621/GeoLite2-City.mmdb')
    response = reader.city(ip_address)
    
    print("response.country.iso_code: {}".format(response.country.iso_code))
    print("response.subdivisions.most_specific.name: {}".format(response.subdivisions.most_specific.name))
    print("response.subdivisions.most_specific.iso_code: {}".format(response.subdivisions.most_specific.iso_code))
    print("response.city.name: {}".format(response.city.name))
    print("response.postal.code: {}".format(response.postal.code))
    
    reader.close()
    
    if response.traits.is_anonymous_proxy or response.traits.is_legitimate_proxy:
        return response.traits.network
    return None

def check_dnsbl(ip_address):
    dnsbl_providers = [
        'zen.spamhaus.org',
        'b.barracudacentral.org',
        'bl.spamcop.net',
        'dnsbl.sorbs.net',
    ]
    
    reversed_ip = '.'.join(reversed(ip_address.split('.')))
    results = {}
    
    for provider in dnsbl_providers:
        try:
            query = f"{reversed_ip}.{provider}"
            answers = dns.resolver.resolve(query, 'A')
            results[provider] = 'Listed'
        except dns.resolver.NXDOMAIN:
            results[provider] = 'Not listed'
        except Exception as e:
            results[provider] = f"Error: {e}"
    
    return results

def check_ip_clean(ip_address):
    # Load VPN/Proxy IP list
    vpn_ip_list = load_vpn_ip_list('./db/vpn_ip_list.txt')
    
    # Check if IP is in known VPN/Proxy list
    if is_ip_in_vpn_list(ip_address, vpn_ip_list):
        return "IP is listed in known VPN/Proxy list."
    
    # Check using GeoLite2 database
    vpn_provider = check_vpn_using_geolocation(ip_address)
    if vpn_provider:
        return f"IP is detected as a VPN/Proxy: {vpn_provider}"
    
    # Check against DNS-based blacklists
    dnsbl_results = check_dnsbl(ip_address)
    for provider, status in dnsbl_results.items():
        if status == 'Listed':
            return f"IP is listed on DNSBL: {provider}"
    
    return "IP is clean."


ip_address = '27.34.66.195'
result = check_ip_clean(ip_address)
result2= check_vpn_using_geolocation(ip_address)
print(result)
print(result2)
