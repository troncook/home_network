# network_scan.py
import nmap

def scan_network(subnet):
    """
    Scan the specified subnet using Nmap's -sn (ping sweep) to discover active hosts.
    Returns a list of dictionaries with IP, MAC, and Vendor data.
    """
    nm = nmap.PortScanner()
    print(f"[*] Scanning subnet {subnet} for active hosts. Please wait...")
    
    # '-sn' does host discovery without port scanning
    nm.scan(hosts=subnet, arguments='-sn')

    active_hosts = []

    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            ip_addr = host
            mac_addr = nm[host]['addresses'].get('mac', 'N/A')
            vendor = nm[host]['vendor'].get(mac_addr, 'Unknown')

            host_info = {
                "ip": ip_addr,
                "mac": mac_addr,
                "vendor": vendor
            }
            active_hosts.append(host_info)

    return active_hosts

if __name__ == "__main__":
    # Replace '' with the subnet you want to scan
    subnet_to_scan = ""
    
    hosts = scan_network(subnet_to_scan)

    print(f"[*] Hosts discovered on {subnet_to_scan}:")
    for idx, h in enumerate(hosts, start=1):
        print(f"{idx}. IP: {h['ip']}, MAC: {h['mac']}, Vendor: {h['vendor']}")