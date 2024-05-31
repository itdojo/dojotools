import re


def format_mac_address(mac, case="lower", seperator=":"):
    """
    Format a MAC address into a standardized representation.

    This function takes a MAC address in various formats and converts it into a 
    standardized format. Non-hexadecimal characters are removed, and then colons (or 
    another specified separator) are inserted every two characters. The function 
    also allows specifying the case of the output (either lower or upper).

    Parameters:
    - mac (str): The MAC address to be formatted.
    - case (str, optional): The case of the output MAC address. 
      Options are 'lower' (default) or 'upper'.
    - separator (str, optional): The character to separate hex digits in the MAC address. 
      Default is ':'. If set to None, no separator is used.

    Returns:
    - str: The formatted MAC address.

    Examples:
    >>> format_mac_address("00:c0:ca:32:bd:25")
    '00:c0:ca:32:bd:25'

    >>> format_mac_address("00c0.ca32.bd25", case="upper", separator="-")
    '00-C0-CA-32-BD-25'

    >>> format_mac_address("00-c0-ca-32-bd-25", separator=None)
    '00c0ca32bd25'
    """
    # Remove all non-hexadecimal characters
    clean_mac = re.sub(r'[^0-9a-fA-F]', '', mac)

    # Insert colons every two characters
    if seperator == None:
        seperator = ""
    formatted_mac = seperator.join(clean_mac[i:i+2] for i in range(0, len(clean_mac), 2))

    if case == "upper":
        return formatted_mac.upper()
    else:
        return formatted_mac.lower()
