"""
This module provides functionalities related to wireless network interface 
management on Debian/Ubuntu versions of Linux. It includes capabilities for 
identifying wireless interfaces and allowing the user to select one of 
these interfaces interactively.

It uses various utilities from the 'devtools' package to support its 
operations. This includes detecting the operating system, looking up the 
OUI (Organizationally Unique Identifier) of MAC addresses, and drawing 
lines for aesthetic terminal output.

Functions:
    get_wlan_interfaces():
        Scans and retrieves available WLAN interfaces and their 
        respective MAC addresses.

    interface_selector(wlan_interfaces, showmac=True, linetype=1):
        Provides an interactive interface for selecting a WLAN 
        interface from the list of available interfaces.

Note:
    - The module is specifically designed for use on Debian/Ubuntu 
    Linux distributions.
    - It heavily relies on the structure of the '/sys/class/net' 
    directory for gathering network interface information.
"""

import os
from sys import exit
import dojoutils.getos as getos
import dojoutils.ouilookup
from dojoutils.draw_line import drawline


def get_wlan_interfaces():
    """
    Scans the system to identify available wireless network interfaces 
    along with their MAC addresses.

    This function checks for WLAN interfaces by inspecting the 
    '/sys/class/net' directory. It filters out non-wireless interfaces and 
    retrieves the MAC addresses for the wireless ones.

    Returns:
    dict: A dictionary where keys are interface names and values are 
    their respective MAC addresses.

    Raises:
    SystemExit: If the operating system is not Linux, as the function 
    is designed specifically for Debian/Ubuntu Linux.
    """
    if getos.os_is() != "Linux":
        print("\nThis tool only runs on Debian/Ubuntu versions of Linux.\nExiting.\n")
        return None
    
    if_dir = "/sys/class/net"
    interfaces = os.listdir(if_dir)
    wlan_interfaces = {}
    for iface in interfaces:
        wireless_dir = os.path.join(if_dir, iface, 'wireless')
        if os.path.isdir(wireless_dir):
            address_file = os.path.join(if_dir, iface, 'address')
            if os.path.isfile(address_file):
                with open(address_file, 'r') as f:
                    mac_address = f.read().strip()
            wlan_interfaces[iface] = mac_address

    return wlan_interfaces


def interface_selector(showmac=True, linetype=1):
    """
    Provides an interactive interface for selecting a wireless network 
    interface from a given list.

    This function displays a list of available WLAN interfaces. If 
    'showmac' is True, it also shows the MAC address and the corresponding 
    OUI vendor name for each interface. The user can select an interface by 
    entering its corresponding number.

    Parameters:
    wlan_interfaces (dict): A dictionary of WLAN interfaces and their
      MAC addresses.
    showmac (bool, optional): Whether to show MAC addresses and OUI 
    vendor names. Defaults to True.
    linetype (int, optional): The type of line to be drawn for aesthetic 
    separation. Defaults to 1 (solid line).

    Returns:
    str | None: The selected interface name, or None if the user quits 
    or fails to select a valid interface within the allowed attempts.

    Note:
    - The user has a limited number of attempts (default 3) to make a 
    valid selection.
    - The function allows refreshing the list of interfaces or quitting 
    the selection process.
    """

    wlan_interfaces = get_wlan_interfaces()
    
    print(" WLAN Interface Selector")
    drawline(linetype)
    for count, (interface, mac_address) in enumerate(wlan_interfaces.items(), start=1):
        if showmac:
            oui = ouilookup.oui_lookup(mac_address)
            print(f"{count}. {interface}  ({mac_address}) ({oui.strip()})")
        else:
            print(f"{count}.  {interface}")
    print()

    max_attempts = 3

    while attempt_count < max_attempts:
        choice = input("#️⃣  Enter WLAN interface by number ('q' to quit, 'r' to refresh): ").strip()
        if choice.lower() == 'r':
            wlan_interfaces = get_wlan_interfaces()
            refresh = interface_selector(wlan_interfaces, showmac)
            if refresh is None:
                return None
        elif choice.lower() == 'q':
            print("Quitting WLAN Interface Selection.")
            return None

        if choice.isdigit() and 1 <= int(choice) <= len(wlan_interfaces.keys()):
            return [x for x in wlan_interfaces.keys()][int(choice) - 1]
        else:
            print("❌  Invalid. Enter a number from the list (1, 2, etc.).\n")
            attempt_count += 1

    print("Maximum attempts reached. Exiting.")
    return None







