# main.py
from auto_subnet import get_local_subnet
from network_scan import scan_network
from packet_capture import live_capture

def main():
    # 1. Get subnet automatically
    subnet = get_local_subnet()
    if subnet is None:
        print("Unable to determine subnet. Please set manually.")
        return
    
    print(f"[*] Detected local subnet: {subnet}")

    # 2. Perform Nmap scan
    hosts = scan_network(subnet)
    print("[*] Nmap scan results:")
    for idx, h in enumerate(hosts, start=1):
        print(f"{idx}. IP: {h['ip']}, MAC: {h['mac']}, Vendor: {h['vendor']}")
    
    # 3. Prompt user if they want to capture packets
    choice = input("\nDo you want to start a packet capture? (y/n) ")
    if choice.lower().startswith('y'):
        target_ip = input("Enter the target IP to filter (or press Enter for all): ")
        if not target_ip.strip():
            target_ip = None
        live_capture(interface='Ethernet', target_ip=target_ip, capture_count=10)

if __name__ == "__main__":
    main()