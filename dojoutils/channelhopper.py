#!/usr/bin/env python3 

import threading
from time import sleep
from random import choice
from subprocess import run
from os import geteuid


# Supported channels for 2.4GHz, 5GHz, and 6GHz - Primary 20MHz channels only
CHANNELS = {
    # Primary channel list for 2.4GHz, 5GHz, and 6GHz bands (20MHz wide channels).
    "2.4GHz": [
        "1", "2", "3", "4", "5", "6", "7", "8", "9" , "10", "11"
        ],
    "5GHz": [
        "36", "40", "44", "48", "52", "56", "60", "64", "100", 
        "104", "108", "112", "116", "120", "124", "128", "132", 
        "136", "140", "144", "149", "153", "157", "161", "165"
        ],
    "6GHz": [
        "1", "5", "9", "13", "17", "21", "25", "29", "33", "37", "41", 
        "45", "49", "53", "57", "61", "65", "69", "73", "77", "81", 
        "85", "89", "93", "97", "101", "105", "109", "113", "117", "121", 
        "125", "129", "133", "137","141", "145", "149", "153", "157", 
        "161", "165", "169", "173", "177", "181", "185", "189", "193", 
        "197", "201", "205", "209", "213", "217", "221", "225", "229", 
        "233"
        ]
}

# Default channel list; most likely to be supported by most adapters
DEFAULT_CHANNELS = CHANNELS["2.4GHz"] + CHANNELS["5GHz"]
# print(f"Default channels: {DEFAULT_CHANNELS}")

# List of supported adapters and their supported channels
ADAPTERS = {
    # Adapter: Supported channels. Currently, only primary 20MHz channels are listed.
    # Add more channels if the adapter supports wider channels.
    # Example: "awus036nha": ["1", "6", "11", "36", "40", "44", "48"]
    # Only Alfa Network adapters are listed here.
    "awus036achm": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awus036ach": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awus1900": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awus036ac": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "aws036acm": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awus036acs": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awus036nha": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awpcie-1900u": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awmc7615p": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awus036axer": CHANNELS["2.4GHz"] + CHANNELS["5GHz"],
    "awus036nh": CHANNELS["2.4GHz"],
    "awmc9886ph": CHANNELS["5GHz"],
    "awus036ax": CHANNELS["2.4GHz"] + CHANNELS["5GHz"] + CHANNELS["6GHz"],
    "awus036axm": CHANNELS["2.4GHz"] + CHANNELS["5GHz"] + CHANNELS["6GHz"],
    "awus036axml": CHANNELS["2.4GHz"] + CHANNELS["5GHz"] + CHANNELS["6GHz"],
}


class RootPrivilegesError(Exception):
    """Exception raised when script is not run as root."""
    pass


def rootcheck():
    """
    Check if the script is running as root. If not, raise an exception.
    """
    if geteuid() != 0:
        raise RootPrivilegesError("❌ Changing WLAN channel requires root (sudo).")


def supported_adapters():
    """
    Print the list of supported wireless adapters and their supported channels.
    """
    return [adapter for adapter in ADAPTERS.keys()]


def channel_mappings():
    """
    Print the supported channel mappings when calling hopper().
    """
    print("Channel mappings:")
    print("  '2.4GHz': Channels 1-11")
    print("  '2.4GHz-all': All 2.4GHz channels (1-13)")
    print("  '5GHz': All 5GHz channels (20MHz primary channels)")
    print("  '5GHz-UNII1': 5GHz Sub-band 1 (36, 40, 44, 48)")
    print("  '5GHz-UNII2': 5GHz Sub-band 2 (52, 56, 60, 64)")
    print("  '5GHz-UNII3': 5GHz Sub-band 3 (149, 153, 157, 161, 165)")
    print("  '6GHz': All 6GHz channels (20MHz primary channels)")
    print("  'all': All 2.4GHz, 5GHz, and 6GHz primary channels")
    print("  Custom list: Provide a list of channels (i.e. [1, 6, 11, 36, 40])")


def get_channel_list(channel_selection):
    """
    Converts user input (channel mapping keyword or custom channel list) 
    into a list of valid channels.
    
    Args:
        channel_selection (str or list): User input defining channel selection.

    Returns:
        list: A list of channels.
    """
    if isinstance(channel_selection, list):  
        # User provided a custom list of channels, return as list of strings
        return [str(channel) for channel in channel_selection] 
    
    # If user provided a string keyword, map it to predefined channels
    channel_mapping = {
        "2.4GHz": CHANNELS["2.4GHz"],   # Channels 1-11
        "2.4GHz-all": CHANNELS["2.4GHz"] + ["12", "13"],  # All 2.4GHz channels
        "5GHz": CHANNELS["5GHz"],  # All 5GHz channels (20MHz primary channels)
        "5GHz-UNII1": ["36", "40", "44", "48"],  # 5GHz Sub-bands
        "5GHz-UNII2": ["52", "56", "60", "64"],  # 5GHz Sub-bands
        "5GHz-UNII3": ["149", "153", "157", "161", "165"],  # 5GHz Sub-bands
        "6GHz": CHANNELS["6GHz"],  # All 6GHz channels (20MHz primary channels)
        "all": CHANNELS["2.4GHz"] + CHANNELS["5GHz"] + CHANNELS["6GHz"]
    }
    return channel_mapping.get(channel_selection, DEFAULT_CHANNELS)  # Default to 2.4 & 5GHz


def hopper(iface, dwell=0.15, channels=DEFAULT_CHANNELS, adapter=None, mode="random", stop_event=None):
    """
    Performs channel hopping on the specified interface.
    Requires root (sudo) privileges.
    
    Usage: hopper(iface, dwell, channels, adapter, mode, stop_event)

    Args:
        iface (str): Network interface.
        dwell (float): Time between channel switches.
        channels (str or list): Can be "2.4GHz", "5GHz", "all", or a custom list (i.e. [1,6,11,36,40]).
        adapter (str): Optional; if specified, will override `channels` based on adapter capabilities.
        mode (str): "random" (default) or "sequential" for sequential channel hopping.
        stop_event (threading.Event): Optional event to stop the channel hopper.
    """
    
    # Import here to avoid circular import
    from dojoutils.wifi.channelhopper import get_channel_list, ADAPTERS, DEFAULT_CHANNELS  # Ensure import works
    
    # Determine the channel list
    if adapter:
        channels = ADAPTERS.get(adapter, DEFAULT_CHANNELS)
    else:
        channels = get_channel_list(channels)

    index = 0  # Used for sequential mode
    while not (stop_event and stop_event.is_set()):  # Stop if stop_event is set
        try:
            if mode == "sequential":
                channel = channels[index]  # Pick the next channel sequentially
                index = (index + 1) % len(channels)  # Loop back when reaching the end
            else:
                channel = choice(channels)  # Default to random selection

            #print(f"Setting {iface} to channel {channel}")
            cmd = f"iw dev {iface} set channel {channel}"
            run(cmd, shell=True, check=True)
            sleep(dwell)
        except KeyboardInterrupt:
            print("Exiting channel hopper")
            break
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == "__main__":
    check_root()
    iface = input("WiFi interface name: ")
    dwell = float(input("Dwell time (default=0.15): ") or 0.15)
    channels = input("Channel selection (2.4GHz, 5GHz, 6GHz, all, or custom list): ") or DEFAULT_CHANNELS
    adapter = input("Adapter name (optional): ")
    mode = input("Channel hopping mode ('random' or 'sequential'): ") or "random"
    hopper(iface, dwell=0.2, channels="2.4GHz", mode="random")
