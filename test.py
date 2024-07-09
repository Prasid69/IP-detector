import geoip2.database
import ipaddress
import dns.resolver
import concurrent.futures

def load_vpn_ip_list(file_path):
    with open(file_path, 'r') as file:
        vpn_ips = file.read().splitlines()
    return vpn_ips

def is_ip_in_vpn_list(ip_address, vpn_ips):
    ip = ipaddress.ip_address(ip_address)
    vpn_networks = [ipaddress.ip_network(vpn_ip) if '/' in vpn_ip else ipaddress.ip_network(vpn_ip + '/32') for vpn_ip in vpn_ips]
    return any(ip in vpn_network for vpn_network in vpn_networks)

def check_vpn_using_geolocation(ip_address, reader):
    response = reader.city(ip_address)
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
    
    def query_dnsbl(provider):
        try:
            query = f"{reversed_ip}.{provider}"
            dns.resolver.resolve(query, 'A')
            return provider, 'Listed'
        except dns.resolver.NXDOMAIN:
            return provider, 'Not listed'
        except Exception as e:
            return provider, f"Error: {e}"
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = dict(executor.map(query_dnsbl, dnsbl_providers))
    
    return results

def check_ip_clean(ip_address, vpn_ip_list, geoip_reader):
    # Check if IP is in known VPN/Proxy list
    if is_ip_in_vpn_list(ip_address, vpn_ip_list):
        return "IP is listed in known VPN/Proxy list."
    
    # Check using GeoLite2 database
    vpn_provider = check_vpn_using_geolocation(ip_address, geoip_reader)
    if vpn_provider:
        return f"IP is detected as a VPN/Proxy: {vpn_provider}"
    
    # Check against DNS-based blacklists
    dnsbl_results = check_dnsbl(ip_address)
    for provider, status in dnsbl_results.items():
        if status == 'Listed':
            return f"IP is listed on DNSBL: {provider}"
    
    return "IP is clean."

# Load VPN/Proxy IP list once
vpn_ip_list = load_vpn_ip_list('./db/vpn_ip_list.txt')

# Open GeoIP reader once
geoip_reader = geoip2.database.Reader('./db/GeoLite2-City_20240621/GeoLite2-City.mmdb')

# Check IP address
ip_address = '171.22.248.206'
result = check_ip_clean(ip_address, vpn_ip_list, geoip_reader)
print(result)

# Close GeoIP reader
geoip_reader.close()
