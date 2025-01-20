import pyshark

def live_capture(interface='Ethernet', target_ip=None, capture_count=20):
    """
    Captures 'capture_count' packets from 'interface' using Pyshark.
    Optionally filters for traffic related to 'target_ip'.
    """

    # Build a Wireshark-style display filter if an IP is provided.
    # This filter will capture only packets from or to the target_ip.
    # For example, 'ip.addr == 1xx.1xx.0.xx'
    display_filter = None
    if target_ip:
        display_filter = f"ip.addr == {target_ip}"

    print(f"[*] Starting live capture on interface: {interface}")
    if display_filter:
        print(f"[*] Using display filter: {display_filter}")

    capture = pyshark.LiveCapture(interface=interface, display_filter=display_filter)

    packet_counter = 0
    for packet in capture.sniff_continuously():
        packet_counter += 1
        try:
            # Print a quick summary of each packet
            highest_layer = packet.highest_layer
            src = packet.ip.src if 'IP' in packet else 'Unknown'
            dst = packet.ip.dst if 'IP' in packet else 'Unknown'
            print(f"Packet #{packet_counter}: {highest_layer}, {src} -> {dst}")
        except AttributeError:
            # Some packets may not have standard IP layers
            print(f"Packet #{packet_counter}: {packet}")

        if packet_counter >= capture_count:
            break

    print("[*] Capture complete.")

if __name__ == "__main__":
    # Example usage:
    # - interface could be 'Ethernet' or 'Wi-Fi' or the actual name on your system
    # - target_ip can be set to the device IP you're investigating
    # - replace '' with your ip
    live_capture(interface='Ethernet', target_ip='', capture_count=20)
