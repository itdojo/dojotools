"""
This module provides a function to draw decorative lines in the terminal.

The function 'draw_line' prints a line composed of a specific character, 
spanning the entire width of the terminal window. It leverages the 
os.get_terminal_size method to dynamically determine the width of the 
terminal at runtime, ensuring that the printed line always fits perfectly 
across the terminal window, regardless of its current size.

Functions:
    draw_line(linetype=1): Prints a line of a specified type across the terminal window.

Available Line Types:
    1: Solid line (─)
    2: Dotted line (∙)
    3: Diamond line (⌶)
    4: Star line (☆)
    5: Double line (⏥)
    Any other value defaults to a solid line (─).

The function is primarily intended for use in console-based applications 
where visually distinct sections are required for better readability or 
aesthetic appeal.

Example:
    >>> draw_line(3)
    This will print a line of diamonds spanning the width of the terminal.

Returns:
    True: Indicates successful execution and line printing.
"""

from os import get_terminal_size

def draw_line(linetype=1):
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
            print('─' * terminal_size.columns)
        case 2:
            print('∙' * terminal_size.columns)
        case 3:
            print('⌶' * terminal_size.columns)
        case 4:
            print('☆' * terminal_size.columns)
        case 5:
            print('⏥' * terminal_size.columns)
        case _:
            print('─' * terminal_size.columns)
    return None
