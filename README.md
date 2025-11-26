# Advanced Calculator

A secure, high-performance mathematical formula parser and evaluator with variable substitution support.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Advanced Calculator                         │
├─────────────────────────────────────────────────────────────────┤
│  Input: "sqrt(x) + (x*y)/2"  with  x=3, y=8                     │
│                              │                                   │
│                              v                                   │
│                    ┌─────────────────┐                          │
│                    │  Safe AST-based │                          │
│                    │    Evaluator    │                          │
│                    └─────────────────┘                          │
│                              │                                   │
│                              v                                   │
│  Output: 13.732050807568877                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Features

| Category | Details |
|----------|---------|
| **Security** | AST-based evaluation (no `eval()`) with whitelisted functions only |
| **Performance** | ~0.0003s average per evaluation |
| **Test Coverage** | 2,670+ test cases including edge cases |
| **Dependencies** | Python standard library only |

## Supported Operations

```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│   Arithmetic   │  Trigonometry  │   Functions    │   Constants    │
├────────────────┼────────────────┼────────────────┼────────────────┤
│  +   Addition  │  sin(x)        │  sqrt(x)       │  PI            │
│  -   Subtract  │  cos(x)        │  log(x)        │                │
│  *   Multiply  │  tan(x)        │  abs(x)        │                │
│  /   Divide    │                │  floor(x)      │                │
│                │                │  ceil(x)       │                │
│                │                │  factorial(x)  │                │
│                │                │  mod(x, y)     │                │
│                │                │  pow(x, y)     │                │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

## Installation

```bash
git clone https://github.com/ldziura/Advanced_Calculator.git
cd Advanced_Calculator
```

No external dependencies required.

## Usage

### Command Line Interface

```bash
python main.py
```

```
Enter a formula: sqrt(x) + (x*y)/2
Enter the number of unknowns: 2
Enter the name of the unknown 1: x
Enter the value of x: 3
Enter the name of the unknown 2: y
Enter the value of y: 8

sqrt(x) + (x*y)/2 with {'x': 3.0, 'y': 8.0} = 13.732050807568877
```

### As a Module

```python
from ComputeFormula import compute_formula

# Simple expression
result = compute_formula("sqrt(x) + PI", {"x": 16})
# Returns: 7.141592653589793

# Complex nested expression
result = compute_formula(
    "pow(mod(x, 10) + floor(y), 2)",
    {"x": 27, "y": 3.7}
)
# Returns: 100.0
```

## API Reference

### `compute_formula(input_string, unknown_value)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `input_string` | `str` | Mathematical formula to evaluate |
| `unknown_value` | `dict[str, float]` | Variable names mapped to values |
| **Returns** | `float \| str` | Result or error message |

### Error Handling

| Error Type | Cause |
|------------|-------|
| `ValueError` | Invalid variable name or non-numeric value |
| `ZeroDivisionError` | Division by zero |
| `NameError` | Undefined variable or function |
| `"Formula is not well formed"` | Invalid syntax |
| `"Parentheses are not matched"` | Unbalanced parentheses |
| `"Can't sqrt with value..."` | Square root of negative number |

## Architecture

```
ComputeFormula.py
├── SafeEvaluator (class)      # AST-based secure expression evaluator
│   ├── SAFE_OPERATORS         # Whitelisted: +, -, *, /, **
│   ├── SAFE_FUNCTIONS         # Whitelisted: sqrt, sin, cos, etc.
│   └── SAFE_CONSTANTS         # Whitelisted: math.pi
│
├── Validation Functions
│   ├── is_well_formed()       # Syntax validation
│   ├── check_parentheses()    # Balance check
│   ├── is_word()              # Variable name validation
│   └── is_number()            # Numeric type check
│
└── compute_formula()          # Main entry point
```

## Testing

```bash
python test_ComputeFormula.py
```

### Test Coverage

| Test Category | Cases | Description |
|---------------|-------|-------------|
| Basic Operations | 16 | Arithmetic, trig, log functions |
| Invalid Formulas | 25 | Syntax errors, undefined vars |
| Random Values | 1,500 | Randomized inputs (-100 to 100) |
| Extreme Values | 660 | 2^32, 2^64, infinitesimals |
| Complex Nested | 480 | Deeply nested expressions |

```
----------------------------------------------------------------------
Ran 6 tests in 0.090s

OK
```

## Security

This calculator uses AST (Abstract Syntax Tree) parsing instead of `eval()` to prevent code injection attacks. Only explicitly whitelisted operations are permitted:

```
Blocked: __import__, exec, eval, open, os.*, sys.*, etc.
Allowed: math.sqrt, math.sin, math.cos, math.tan, math.log,
         math.fmod, math.pow, math.factorial, math.fabs,
         math.floor, math.ceil, math.pi
```

## Project Structure

```
Advanced_Calculator/
├── ComputeFormula.py       # Core evaluation engine
├── main.py                 # CLI interface
├── test_ComputeFormula.py  # Test suite
├── README.md               # Documentation
└── .gitignore              # Git ignore rules
```

## License

This project is open source and available for use in larger projects.
