import os.path
import re
import dojoutils.network.macformatter as macformatter
import requests

OUI_URL = "https://standards-oui.ieee.org/oui/oui.txt"
OUI_FILE = "oui.txt"

def oui_lookup(mac_address: str, case="upper", seperator="") -> str:
    if not check_for_oui_file():
        if not download_oui_file():
            return "OUI file download failed"

    formatted_mac = macformatter.format_mac_address(mac_address, case, seperator)
    formatted_mac = re.sub(r"[^A-F0-9]", "", formatted_mac)
    node_oui = formatted_mac[:6]

    try:
        with open(OUI_FILE, 'r', encoding="utf-8") as f:
            filedata = f.readlines()
            for line in filedata:
                if node_oui in line:
                    vendor = line.replace("\t", "").replace("(base 16)", "").replace("\n", "")[8:].strip()
                    return vendor
    except FileNotFoundError:
        return "OUI file not found"
    except Exception as e:
        print(f"Error reading OUI file: {e}")
    return "Vendor Unknown"


def check_for_oui_file() -> bool:
    """
    Checks for the existence of the 'oui.txt' file in the local directory.

    Returns:
    bool: True if the 'oui.txt' file exists in the local directory, else False.
    """
    return os.path.isfile(OUI_FILE)


def download_oui_file() -> bool:
    """
    Downloads the OUI data file from the IEEE website.

    Returns:
    bool: True if the file is downloaded and saved successfully, False otherwise.
    """
    try:
        print(f"Downloading {OUI_FILE} from IEEE.org...")
        response = requests.get(OUI_URL, stream=True)
        response.raise_for_status()

        with open(OUI_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):  # Handle large downloads
                f.write(chunk)

        print(f"{OUI_FILE} downloaded successfully.")
        return True
    except requests.RequestException as e:
        print(f"Error downloading {OUI_FILE}: {e}")
        return False