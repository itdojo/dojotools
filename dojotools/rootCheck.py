"""
This module provides functionality for checking if the 
script is run with root privileges.

It uses the os module to check the effective user ID of 
the process. The script exits if it is not run as root.
"""

from os import geteuid
from sys import exit

def check_root():
    """
    Check if the script is run with root (sudo) privileges.

    Exits the script with a status code of 1 if it is not run as 
    root, after printing an error message.

    Side effects:
        - Exits the script if not run as root.
    """
    if geteuid() != 0:
        print("\n❌  Run as root.\n")
        exit(1)
