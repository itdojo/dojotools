"""
This module provides functionality for looking up the vendor name 
associated with a given MAC address using the OUI (Organizationally 
Unique Identifier) portion of the address. It uses the OUI data 
from the IEEE standards, which is downloaded and stored locally 
if not already present.

The module contains three main functions:
- oui_lookup: Performs the OUI lookup and returns the vendor name.
- check_for_oui_file: Checks if the OUI data file is present locally.
- download_oui_file: Downloads the OUI data file from the IEEE website 
  if not present.

External Dependencies:
- devools.macFormatter: A custom module for formatting MAC addresses.
- requests: Required for downloading the OUI data file from the internet.

Functions:
    oui_lookup(mac_address, case="upper", seperator=""):
        Looks up the vendor name for a given MAC address.

        Parameters:
        mac_address (str): The MAC address to look up. case (str, optional): 
        The case format for the MAC address ('upper' or 'lower'). 
        Defaults to 'upper'.
        seperator (str, optional): The separator character in the MAC 
        address. Defaults to no separator.

        Returns:
        str: The vendor name associated with the MAC address or 
        'Vendor Unknown' if not found.

    check_for_oui_file():
        Checks if the OUI data file (oui.txt) is present in 
        the local directory.

        Returns:
        bool: True if the file exists, False otherwise.

    download_oui_file():
        Downloads the OUI data file from the IEEE website.

        Returns:
        bool: True if download is successful, False otherwise.

Example:
    >>> oui_lookup("00:1A:2B:3C:4D:5E")
    'Vendor Name'

Note:
- The OUI data file (oui.txt) is obtained from 'http://standards-oui.ieee.org/oui/oui.txt'.
- The MAC address lookup is case-insensitive and can be formatted with any common separators.
"""

import os.path
import re
from dojotools import macFormatter
import requests


def oui_lookup(mac_address, case="upper", seperator=""):
    """
    Performs a lookup to find the vendor name associated with the provided MAC 
    address using the OUI (Organizationally Unique Identifier).

    This function formats the given MAC address as per the specified case and 
    separator, retrieves the first six characters (OUI), and searches for this 
    OUI in the local 'oui.txt' file. If the file doesn't exist, it attempts 
    to download it.

    Parameters:
    mac_address (str): The MAC address for which the vendor lookup is to be performed.
    case (str, optional): Determines the case of the MAC address ('upper' or 'lower'). 
    Defaults to 'upper'.
    seperator (str, optional): The separator to be used in the MAC address. 
    Defaults to no separator. Typical separators are ':' and '-'.

    Returns:
    str: The vendor name associated with the MAC address. Returns 
    'Vendor Unknown' if not found.

    Raises:
    FileNotFoundError: If 'oui.txt' is not found and cannot be downloaded.
    """
    if not check_for_oui_file():
        download_oui_file()

    ouifile = "oui.txt"

    mac_address = macFormatter.format_mac_address(mac_address, case, seperator)
    mac_address = re.sub(r"[^A-F0-9]", "", mac_address)
    node_oui = mac_address[:6]

    with open(ouifile, 'r') as f:
        filedata = f.readlines()
        for line in filedata:
            if node_oui in line:
                vendor = line.replace("\t", "").replace("(base 16)", "").replace("\n", "")[8:].strip()
                return vendor
        return "Vendor Unknown"


def check_for_oui_file():
    """
    Checks for the existence of the 'oui.txt' file in the local directory.

    This function is used to verify if the OUI data file, which contains the 
    mappings of OUIs to vendor names, is present.
    The file is expected to be named 'oui.txt'.  If it is not present, Internet
    connectivity is required to download it from the IEEE website.

    Returns:
    bool: True if the 'oui.txt' file exists in the local directory, 
    False otherwise.
    """
    oui_txtfile = "oui.txt"  # http://standards-oui.ieee.org/oui/oui.txt

    oui_txt = os.path.isfile(oui_txtfile)
    if oui_txt:
        return True
    else:
        return False


def download_oui_file():
    """
    Downloads the OUI data file from the IEEE website.

    This function is invoked to download the 'oui.txt' file from the official 
    IEEE website if it's not present locally.
    The file contains the necessary data for OUI to vendor name mapping.

    Returns:
    bool: True if the file is downloaded and saved successfully, False otherwise.

    Raises:
    requests.exceptions.HTTPError: If there is a problem with the network request.
    """
    import requests

    oui_url = "http://standards-oui.ieee.org/oui/oui.txt"
    ouifile = "oui.txt"

    try:
        print("Downloading oui.txt from ieee.org...")
        r = requests.get(oui_url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error downloading oui.txt: {err}")
        return False

    with open(ouifile, "wb") as f:
        f.write(r.content)

    return True
