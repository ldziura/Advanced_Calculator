"""
Advanced Calculator - Main Entry Point

This module provides a command-line interface for the formula calculator.
Users can input mathematical formulas with variables and get computed results.
"""

from ComputeFormula import compute_formula


def is_valid_number(value: str) -> bool:
    """
    Check if a string represents a valid number (int or float, positive or negative).

    Args:
        value: The string to validate

    Returns:
        True if the string is a valid number, False otherwise
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def input_and_solve() -> str:
    """
    Interactive function that prompts user for formula input and computes the result.

    Prompts the user for:
    - A mathematical formula
    - The number of unknown variables
    - Names and values for each variable

    Returns:
        The computed result as a string

    Example session:
        Enter a formula: sqrt(x) + (x*y)/2
        Enter the number of unknowns: 2
        Enter the name of the unknown 1: x
        Enter the value of x: 3
        Enter the name of the unknown 2: y
        Enter the value of y: 8
        sqrt(x) + (x*y)/2 with {'x': 3.0, 'y': 8.0} = 13.732050807568877
    """
    input_formula = input("Enter a formula: ")

    number_of_unknowns = input("Enter the number of unknowns: ")

    # Validate number of unknowns
    if not number_of_unknowns.isdigit():
        print("Error: Number of unknowns must be a positive integer")
        return ""

    unknown_dict = {}
    for i in range(int(number_of_unknowns)):
        unknown_name = input(f"Enter the name of the unknown {i + 1}: ")

        # Validate unknown name is alphabetic
        if not unknown_name.isalpha():
            print("Error: Unknown name must contain only letters")
            return ""

        unknown_value = input(f"Enter the value of {unknown_name}: ")

        # Validate unknown value is a number (supports floats and negatives)
        if not is_valid_number(unknown_value):
            print("Error: Unknown value must be a number (e.g., 5, -3, 3.14, -2.5)")
            return ""

        unknown_dict[unknown_name] = float(unknown_value)

    try:
        result = compute_formula(input_formula, unknown_dict)
        print(f"{input_formula} with {unknown_dict} = {result}")
        return str(result)
    except Exception as e:
        print(f"Error: {e}")
        return ""


if __name__ == "__main__":
    input_and_solve()
