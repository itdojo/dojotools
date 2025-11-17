"""
This module provides a function to draw decorative lines in the terminal.

The function 'drawline()' prints a line composed of a specific unicode character 
spanning the entire width of the terminal window. It leverages os.get_terminal_size 
method to dynamically determine terminal width when function is called.  This ensures
printed line always fits perfectly across the terminal window.

Functions:
    drawline(linetype=1): Prints a line of a specified type across the terminal window.

Available Line Types:
    1: Solid line   (────────────────)
    2: Dotted line  (∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙)
    3: I-Beam line  (⌶⌶⌶⌶⌶⌶⌶⌶⌶⌶⌶⌶⌶⌶)  prints solid, no space between characters
    4: Star line    (☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆)
    5: Solid Star   (✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯)
    6: Double line  (⏥⏥⏥⏥⏥⏥⏥⏥⏥)  prints solid, no space between characters
    7: Diamond line (♢♢♢♢♢♢♢♢♢♢♢♢♢♢♢♢)
    8: Box line     (⎕⎕⎕⎕⎕⎕⎕⎕⎕⎕⎕⎕⎕⎕⎕⎕)
    Any other value defaults to a solid line (────────────────).

This is intended for use in console-based applications where visually distinct 
sections are required for better readability or aesthetic appeal.

Example:
    >>> drawline(4)
    This will print a line of stars spanning the width of the terminal.

Usage: 
    import into your script and call the function. Example:

    from drawline import drawline
    drawline()
    
Returns:
    True: Indicates successful execution and line printing.
"""

from os import get_terminal_size


def drawline(linetype=1):
    """
    Prints a line composed of a specified character type, spanning the entire width of the terminal.

    Parameters:
    linetype (int, optional): Specifies the type of line to be drawn. Defaults to 1 (solid line).

    Returns:
    bool: True if the line is printed successfully.
    """
    terminal_size = get_terminal_size()
    match linetype:
        case 1:
            linestyle = '─'  # solid line
        case 2:
            linestyle = '∙'  # dotted line
        case 3:
            linestyle = '⌶'  # I-beam line
        case 4:
            linestyle = '☆'  # star line (outline)
        case 5:
            linestyle = '✯'  # star line (solid)
        case 6:
            linestyle = '⏥'  # double line
        case 7: 
            linestyle = '♢'  # diamond line
        case 8:
            linestyle = '⎕'  # box line
        case _:
            linestyle = '─'  # sold line
    print(f"{linestyle * terminal_size.columns}")
    return None
