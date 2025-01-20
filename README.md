# Home Network Investigation

This repository demonstrates how to:
1. **Automatically detect your local subnet** using `netifaces`.
2. **Scan** that subnet with **Nmap** (via `python-nmap`).
3. **Capture** network traffic using **Pyshark**.

> **Disclaimer**: Only use these tools on networks you own or have explicit permission to scan and capture.

## Prerequisites

- **Python 3.x**  
- **Nmap** installed on your system and in PATH (so `nmap --version` works).  
- **Wireshark/TShark** installed for Pyshark (so `tshark --version` works).  

## Installation

1. **Clone** the repository:
   ```bash
   git clone https://github.com/YourUsername/home-network-investigation.git
