"""
Advanced Calculator - Formula Computation Module

This module provides functionality to parse and evaluate mathematical formulas
with variable substitution. It supports various mathematical operations including
arithmetic, trigonometry, logarithms, and more.
"""

import ast
import math
import operator
import re
import logging
from typing import Optional, Union

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # Set to DEBUG for verbose output


# Safe operators for AST evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Safe math functions allowed in formulas
SAFE_FUNCTIONS = {
    'math.sqrt': math.sqrt,
    'math.log': math.log,
    'math.sin': math.sin,
    'math.cos': math.cos,
    'math.tan': math.tan,
    'math.fmod': math.fmod,
    'math.pow': math.pow,
    'math.factorial': math.factorial,
    'math.fabs': math.fabs,
    'math.floor': math.floor,
    'math.ceil': math.ceil,
}

# Safe constants
SAFE_CONSTANTS = {
    'math.pi': math.pi,
}


class SafeEvaluator:
    """
    A safe expression evaluator that uses AST parsing instead of eval().
    Only allows mathematical operations, no arbitrary code execution.
    """

    def __init__(self) -> None:
        self.operators = SAFE_OPERATORS
        self.functions = SAFE_FUNCTIONS
        self.constants = SAFE_CONSTANTS

    def evaluate(self, expression: str) -> Union[int, float]:
        """
        Safely evaluate a mathematical expression.

        Args:
            expression: A string containing a mathematical expression

        Returns:
            The numerical result of the expression

        Raises:
            ValueError: If the expression contains unsafe operations
            ZeroDivisionError: If division by zero occurs
            NameError: If an undefined variable is encountered
        """
        try:
            tree = ast.parse(expression, mode='eval')
            return self._eval_node(tree.body)
        except ZeroDivisionError:
            raise ZeroDivisionError(f"Can't divide by 0 in {expression}")
        except (SyntaxError, TypeError) as e:
            raise ValueError(f"Invalid expression: {expression} - {e}")

    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        """Recursively evaluate an AST node."""

        if isinstance(node, ast.Constant):
            # Handle numeric constants (Python 3.8+)
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        elif isinstance(node, ast.Num):
            # Handle numeric literals (Python 3.7 compatibility)
            return node.n

        elif isinstance(node, ast.BinOp):
            # Handle binary operations: +, -, *, /, **
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)

            if op_type not in self.operators:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")

            return self.operators[op_type](left, right)

        elif isinstance(node, ast.UnaryOp):
            # Handle unary operations: -, +
            operand = self._eval_node(node.operand)
            op_type = type(node.op)

            if op_type not in self.operators:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

            return self.operators[op_type](operand)

        elif isinstance(node, ast.Call):
            # Handle function calls: math.sqrt(), math.sin(), etc.
            func_name = self._get_func_name(node.func)

            if func_name not in self.functions:
                raise NameError(f"Unsupported function: {func_name}")

            args = [self._eval_node(arg) for arg in node.args]
            return self.functions[func_name](*args)

        elif isinstance(node, ast.Attribute):
            # Handle attributes like math.pi
            attr_name = self._get_attr_name(node)

            if attr_name in self.constants:
                return self.constants[attr_name]

            raise NameError(f"Unsupported attribute: {attr_name}")

        elif isinstance(node, ast.Name):
            # Handle named constants - raise NameError for undefined variables
            raise NameError(f"name '{node.id}' is not defined")

        elif isinstance(node, ast.Expression):
            return self._eval_node(node.body)

        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")

    def _get_func_name(self, node: ast.AST) -> str:
        """Extract the full function name from a Call node."""
        if isinstance(node, ast.Attribute):
            return f"{self._get_attr_name_base(node.value)}.{node.attr}"
        elif isinstance(node, ast.Name):
            return node.id
        raise ValueError(f"Cannot determine function name from {type(node)}")

    def _get_attr_name(self, node: ast.Attribute) -> str:
        """Extract the full attribute name."""
        return f"{self._get_attr_name_base(node.value)}.{node.attr}"

    def _get_attr_name_base(self, node: ast.AST) -> str:
        """Extract the base name of an attribute."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_attr_name_base(node.value)}.{node.attr}"
        raise ValueError(f"Cannot determine attribute base from {type(node)}")


# Global safe evaluator instance
_safe_evaluator = SafeEvaluator()


def safe_eval(expression: str) -> Union[int, float]:
    """
    Safely evaluate a mathematical expression without using eval().

    Args:
        expression: A string containing a mathematical expression

    Returns:
        The numerical result of the expression
    """
    return _safe_evaluator.evaluate(expression)


def get_sqrt_value(formula_string: str) -> str:
    """
    Extract the operand from a math.sqrt() call in a formula string.

    Args:
        formula_string: A string that may contain math.sqrt(...)

    Returns:
        The operand inside the sqrt, or empty string if not found
    """
    pattern = re.compile(r"math\.sqrt\((.+?)\)")
    matches = pattern.findall(formula_string)

    if matches:
        return matches[0]
    return ""


def get_operator_value(formula_string: str, op: str) -> list[str]:
    """
    Extract both operands from a binary operator call like mod(x, y) or pow(x, y).

    Args:
        formula_string: A string containing the operator call
        op: The operator name (e.g., 'mod', 'pow')

    Returns:
        A list containing [first_operand, second_operand]
    """
    # Find the operator and extract content between parentheses
    pattern = re.compile(rf"{op}\((.+)\)")
    match = pattern.search(formula_string)

    if not match:
        return ["", ""]

    content = match.group(1)

    # Parse the two operands, handling nested parentheses
    depth = 0
    split_index = -1

    for i, char in enumerate(content):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char == ',' and depth == 0:
            split_index = i
            break

    if split_index == -1:
        return [content, ""]

    first_operand = content[:split_index].strip()
    second_operand = content[split_index + 1:].strip()

    return [first_operand, second_operand]


def is_word(word: str) -> bool:
    """
    Check if a string contains only alphabetic characters.

    Args:
        word: The string to check

    Returns:
        True if the string contains only letters, False otherwise
    """
    return bool(re.match(r'^[a-zA-Z]+$', word))


def is_number(value: object) -> bool:
    """
    Check if a value is a numeric type.

    Args:
        value: The value to check

    Returns:
        True if value is int or float, False otherwise
    """
    return isinstance(value, (int, float))


def check_parentheses(formula_string: str) -> bool:
    """
    Verify that parentheses are properly balanced in a formula.

    Args:
        formula_string: The formula to check

    Returns:
        True if parentheses are balanced, False otherwise
    """
    stack = []

    for char in formula_string:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            if stack[-1] == '(':
                stack.pop()
            else:
                return False

    return len(stack) == 0


def is_well_formed(formula: str, unknowns: Optional[list[str]] = None) -> bool:
    """
    Validate that a formula has correct syntax and structure.

    Args:
        formula: The formula string to validate
        unknowns: Optional list of variable names allowed in the formula

    Returns:
        True if the formula is well-formed

    Raises:
        ValueError: If parentheses are mismatched or formula is empty
    """
    if not check_parentheses(formula):
        raise ValueError("Parentheses are not matched")

    if formula.isspace() or formula == '':
        raise ValueError("Formula is empty")

    # Build the regex pattern matching the original implementation
    # This is a character class that allows only specific characters
    pattern = r"^\s*[-+*/()0-9.xyz,sqrtlogsincostanfloorceilfactorialabsmodPIpow\s]+\s*$"

    # Add unknowns to the pattern
    if unknowns is not None:
        char_to_add = ''.join(unknowns)
        index = pattern.find("sqrt")
        pattern = pattern[:index] + char_to_add + pattern[index:]

    regex = re.compile(pattern)
    matches = regex.findall(formula)

    if matches:
        return True
    else:
        return False


def _find_negative_sqrt(formula: str) -> Optional[tuple[float, str]]:
    """
    Find if there's a square root of a negative number in the formula.
    Returns (value, formula_at_point) if found, None otherwise.
    """
    # Find all sqrt calls
    sqrt_pattern = re.compile(r'math\.sqrt\(([^)]+)\)')

    for match in sqrt_pattern.finditer(formula):
        arg = match.group(1)
        try:
            # Try to evaluate the argument
            arg_value = safe_eval(arg)
            if arg_value < 0:
                return (arg_value, formula)
        except (ValueError, NameError, ZeroDivisionError):
            pass

    return None


def compute_formula(input_string: str, unknown_value: Optional[dict[str, float]] = None) -> Union[str, float, int]:
    """
    Parse and evaluate a mathematical formula with variable substitution.

    This function takes a mathematical formula as a string, substitutes
    variable values, and computes the result safely without using eval().

    Args:
        input_string: The mathematical formula to evaluate
        unknown_value: Dictionary mapping variable names to their values

    Returns:
        The computed result, or an error message string if evaluation fails

    Raises:
        ValueError: If unknown_value is not a dictionary or contains invalid data
        ZeroDivisionError: If division by zero occurs
        NameError: If undefined variables are used
    """
    # Validate unknown_value parameter
    if unknown_value is not None:
        if not isinstance(unknown_value, dict):
            raise ValueError("unknown_value is not a dictionary")
    else:
        unknown_value = {}

    # Validate formula structure
    try:
        if not is_well_formed(input_string, unknowns=list(unknown_value.keys())):
            return "Formula is not well formed"
    except ValueError as e:
        return str(e)
    except (TypeError, AttributeError) as e:
        logger.error(f"Validation error: {e}")
        return f"Validation error: {e}"

    # Convert formula to use math module functions
    formula = input_string
    formula = formula.replace("PI", "math.pi")
    formula = formula.replace("sqrt(", "math.sqrt(")
    formula = formula.replace("log(", "math.log(")
    formula = formula.replace("sin(", "math.sin(")
    formula = formula.replace("cos(", "math.cos(")
    formula = formula.replace("tan(", "math.tan(")
    formula = formula.replace("mod(", "math.fmod(")
    formula = formula.replace("pow(", "math.pow(")
    formula = formula.replace("factorial(", "math.factorial(")
    formula = formula.replace("abs(", "math.fabs(")
    formula = formula.replace("floor(", "math.floor(")
    formula = formula.replace("ceil(", "math.ceil(")

    # Substitute variable values
    for key, value in unknown_value.items():
        if not is_word(key):
            raise ValueError(f"Unknown key '{key}' is not a valid variable name")

        if not is_number(value):
            raise ValueError(f"Value of '{key}' = {value} is not a number")

        if str(key) in input_string:
            if value is not None:
                formula = formula.replace(str(key), f"({str(value)})")
            else:
                return 'Undefined variable'

    logger.debug(f"Transformed formula: {formula}")

    # Check for square root of negative number
    neg_sqrt = _find_negative_sqrt(formula)
    if neg_sqrt:
        value, formula_at_point = neg_sqrt
        return f"Can't sqrt with value ({value}) in {formula_at_point}"

    # Safely evaluate the complete expression
    try:
        result = safe_eval(formula)
        return result
    except ZeroDivisionError:
        raise ZeroDivisionError(f"Can't divide by 0 in {formula}")
    except ValueError as e:
        error_str = str(e).lower()
        if "math domain error" in error_str:
            # This is likely a sqrt of negative number that wasn't caught
            sqrt_value = get_sqrt_value(formula)
            if sqrt_value:
                try:
                    computed_value = safe_eval(sqrt_value)
                    return f"Can't sqrt with value ({computed_value}) in {formula}"
                except (ValueError, NameError, ZeroDivisionError):
                    return f"Can't sqrt with value ({sqrt_value}) in {formula}"
        raise ValueError(f"Value Error occurred in {formula}: {e}")
    except NameError as e:
        raise NameError(str(e))
