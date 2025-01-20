import netifaces
import ipaddress

def get_all_ipv4_interfaces():
    """
    Enumerate all active IPv4 interfaces (excluding loopback and link-local).
    Returns a list of dicts with interface name, IP, Netmask, and optional is_default flag.
    """
    all_interfaces = netifaces.interfaces()
    valid_intf_info = []

    # Gather default gateways (to know which interface is "primary" for AF_INET)
    gateways = netifaces.gateways()
    default_iface = None
    if 'default' in gateways and netifaces.AF_INET in gateways['default']:
        # default gateway entry is something like: ('1xx.1xx.0.1', 'Ethernet')
        default_iface = gateways['default'][netifaces.AF_INET][1]

    for ifc in all_interfaces:
        addrs = netifaces.ifaddresses(ifc)
        if netifaces.AF_INET not in addrs:
            continue

        # Each interface can have multiple IP addresses (rare but possible)
        for addr_info in addrs[netifaces.AF_INET]:
            ip = addr_info.get('addr')
            mask = addr_info.get('netmask')
            # Exclude loopback (127.x.x.x) or link-local (169.254.x.x)
            if not ip or ip.startswith('127.') or ip.startswith('169.254.'):
                continue
            if ip == '0.0.0.0':
                continue  # Usually means no actual IP

            # Determine if this interface is the default route
            is_default = (ifc == default_iface)

            valid_intf_info.append({
                'interface': ifc,
                'ip': ip,
                'mask': mask,
                'is_default': is_default
            })

    return valid_intf_info

def cidr_from_ip_mask(ip, mask):
    """
    Convert IP + Netmask into a string like '192.168.0.0/24'.
    """
    # Use ipaddress module to do the heavy lifting
    network = ipaddress.ip_network(f"{ip}/{mask}", strict=False)
    return str(network)

def pick_interface(interfaces):
    """
    Prompt the user to pick from the provided list of interfaces.
    Returns the chosen interface dict.
    If there's only 1 interface, automatically return it.
    If there's a "default" interface, we highlight it but still ask user to confirm.
    """
    if not interfaces:
        print("No valid IPv4 interfaces found.")
        return None

    if len(interfaces) == 1:
        print("Only one interface found; automatically selecting it.")
        return interfaces[0]

    print("\nDetected the following interfaces:\n")
    for idx, ifc in enumerate(interfaces, start=1):
        star = "(Default)" if ifc['is_default'] else ""
        print(f"{idx}. {ifc['interface']} - IP: {ifc['ip']}, Mask: {ifc['mask']} {star}")

    choice = input("\nSelect an interface by number: ")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(interfaces):
            return interfaces[idx]
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None

def auto_select_subnet():
    """
    High-level function that:
      1. Enumerates interfaces
      2. Asks user to pick one
      3. Returns the CIDR for that interface
    """
    interfaces = get_all_ipv4_interfaces()
    chosen = pick_interface(interfaces)
    if not chosen:
        return None
    cidr = cidr_from_ip_mask(chosen['ip'], chosen['mask'])
    return cidr

if __name__ == "__main__":
    print("Gathering interfaces...")
    result = auto_select_subnet()
    if result:
        print(f"Subnet for chosen interface: {result}")
    else:
        print("No subnet chosen or no valid interface.")


