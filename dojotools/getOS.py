"""
This module provides functionality for checking the operating system.

It uses the platform module from the Python Standard Library to determine the operating system on which the Python interpreter is running.
"""

import platform

def os_is():
    """
    Determine the name of the operating system.

    This function uses the platform module to identify the operating system.

    Returns:
        str: Pretty name ('Linux', 'Windows', or 'Darwin' (MacOS) of the OS.
    """
    return platform.system()
