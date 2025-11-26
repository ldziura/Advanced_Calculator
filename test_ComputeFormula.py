"""
Advanced Calculator - Test Suite

Comprehensive tests for the formula computation module.
Includes tests for basic operations, error handling, random values,
extreme values, and complex nested formulas.
"""

import math
import random
import unittest

from ComputeFormula import compute_formula


class TestEvaluateFormula(unittest.TestCase):
    """Test cases for the compute_formula function."""

    def test_basic(self):
        """Test basic mathematical operations with a fixed value."""
        formulas = [
            ("x + 1", 8),
            ("x * 2", 14),
            ("x/2", 3.5),
            ("sqrt(x)", math.sqrt(7)),
            ("log(x)", math.log(7)),
            ("sin(x)", math.sin(7)),
            ("cos(x)", math.cos(7)),
            ("tan(x)", math.tan(7)),
            ("mod(x, 2)", 1),
            ("pow(x, 2)", 49),
            ("factorial(x)", 5040),
            ("abs(x)", 7),
            ("floor(x)", 7),
            ("ceil(x)", 7),
            ("PI", math.pi),
            ("PI * 2", math.pi * 2),
        ]

        for formula, expected_result in formulas:
            with self.subTest(formula=formula, expected_result=expected_result):
                unknown_dict = {'x': 7}
                result = compute_formula(formula, unknown_dict)
                self.assertEqual(result, expected_result)

    def test_invalid_formulas(self):
        """Test handling of various invalid formula inputs."""

        # Formulas with undefined variables (should raise NameError)
        nameerror_formulas = [
            "x + y",
            "x * y",
            "sqrt(x + y)",
            "log(x * y)",
            "sin(x + y)",
            "cos(x * y)",
            "mod(pow(x, y), z)",
            "factorial(x + y)",
            "abs(x * y)",
            "absc(x)",
            "tasin(x)",
            "tna(x)",
            "mod(x + sans(x), 2)",
            "factoriales(x)",
        ]

        for formula in nameerror_formulas:
            with self.subTest(formula=formula):
                unknown_dict = {'x': 7}
                with self.assertRaises((NameError, ValueError)):
                    compute_formula(formula, unknown_dict)

        # Not well-formed formulas (invalid function names)
        nwf_formulas = [
            "chips(x)",
            "x/2 + prout(x)",
            "sqrt(x) + full(x)",
            "log(jul(x+2)) + (x)",
            "Roubaix(x)",
            "Velkoz(x)",
        ]

        # Not matching parenthesis
        nmp_formulas = [
            "(x + 1",
            "x + 1)",
            "floor(x + 2",
            " 3*8 + 4* sqrt(x",
            "x + y)) * z",
        ]

        # Empty formula
        empty_formulas = [
            "",
            " ",
            "  ",
            "   ",
            "    ",
        ]

        expected_nwf = "Formula is not well formed"
        expected_pnm = "Parentheses are not matched"
        expected_empty = "Formula is empty"

        test_cases = [
            (nwf_formulas, expected_nwf),
            (nmp_formulas, expected_pnm),
            (empty_formulas, expected_empty),
        ]

        for formulas, expected_result in test_cases:
            for formula in formulas:
                with self.subTest(formula=formula, expected_result=expected_result):
                    unknown_dict = {'x': 7}
                    result = compute_formula(formula, unknown_dict)
                    self.assertEqual(result, expected_result)

    def test_unknown_random(self):
        """Test formulas with random values within a reasonable range."""

        for _ in range(100):
            x = random.uniform(-100, 100)

            formulas = [
                ("x + 1", x + 1),
                ("x * 2", x * 2),
                ("x/2", x / 2),
                ("sqrt(abs(x))", math.sqrt(math.fabs(x))),
                ("log(abs(x))", math.log(math.fabs(x))),
                ("sin(x)", math.sin(x)),
                ("cos(x)", math.cos(x)),
                ("tan(x)", math.tan(x)),
                ("mod(x, 2)", math.fmod(x, 2)),
                ("pow(x, 2)", math.pow(x, 2)),
                ("abs(x)", math.fabs(x)),
                ("floor(x)", math.floor(x)),
                ("ceil(x)", math.ceil(x)),
                ("PI", math.pi),
                ("PI * 2", math.pi * 2),
            ]

            for formula, expected_result in formulas:
                with self.subTest(formula=formula, expected_result=expected_result):
                    unknown_dict = {'x': x}
                    result = compute_formula(formula, unknown_dict)
                    self.assertEqual(result, expected_result)

    def test_unknown_extreme_values(self):
        """Test formulas with extreme values including large numbers and infinitesimals."""

        arbit = [1_000_000_000, 0.1234567899876543210]
        power_two_32 = [2_147_483_648, 4_294_967_296]  # 2^32
        power_two_64 = [9_223_372_036_854_775_808, 18_446_744_073_709_551_616]  # 2^64
        infinitesimal = [
            0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001,
            0.00000001, 0.000000001, 0.0000000001, 0.00000000001, 0.000000000001
        ]

        extreme_cases = [arbit, power_two_32, power_two_64, infinitesimal]

        for case in extreme_cases:
            # Test positive cases
            for value_pos in case:
                x = value_pos

                formulas = [
                    ("x + 1", x + 1),
                    ("x * 2", x * 2),
                    ("x/2", x / 2),
                    ("sqrt(abs(x))", math.sqrt(math.fabs(x))),
                    ("log(abs(x))", math.log(math.fabs(x))),
                    ("sin(x)", math.sin(x)),
                    ("cos(x)", math.cos(x)),
                    ("tan(x)", math.tan(x)),
                    ("mod(x, 2)", math.fmod(x, 2)),
                    ("pow(x, 2)", math.pow(x, 2)),
                    ("abs(x)", math.fabs(x)),
                    ("floor(x)", math.floor(x)),
                    ("ceil(x)", math.ceil(x)),
                    ("PI", math.pi),
                    ("PI * 2", math.pi * 2),
                ]

                for formula, expected_result in formulas:
                    with self.subTest(formula=formula, expected_result=expected_result):
                        unknown_dict = {'x': x}
                        result = compute_formula(formula, unknown_dict)
                        self.assertEqual(result, expected_result)

            # Test negative cases
            for value_neg in case:
                x = -value_neg

                formulas = [
                    ("x + 1", x + 1),
                    ("x * 2", x * 2),
                    ("x/2", x / 2),
                    ("sqrt(abs(x))", math.sqrt(math.fabs(x))),
                    ("log(abs(x))", math.log(math.fabs(x))),
                    ("sin(x)", math.sin(x)),
                    ("cos(x)", math.cos(x)),
                    ("tan(x)", math.tan(x)),
                    ("mod(x, 2)", math.fmod(x, 2)),
                    ("pow(x, 2)", math.pow(x, 2)),
                    ("abs(x)", math.fabs(x)),
                    ("floor(x)", math.floor(x)),
                    ("ceil(x)", math.ceil(x)),
                    ("PI", math.pi),
                    ("PI * 2", math.pi * 2),
                ]

                for formula, expected_result in formulas:
                    with self.subTest(formula=formula, expected_result=expected_result):
                        unknown_dict = {'x': x}
                        result = compute_formula(formula, unknown_dict)
                        self.assertEqual(result, expected_result)

    def test_peculiar_formulas(self):
        """Test complex nested formulas with known expected results."""

        formulas = [
            (
                "sqrt( sqrt(7*7) + sin(cos(12/6) + tan(PI/4)) + (7*9+2) * log(4+8 * sqrt(64))) + (7*(3+2 / (8-6)) - floor(sqrt(PI*5*5))) + tan(PI/4) + 2*PI",
                44.07065812843417
            ),
            ('factorial(ceil(sin(7)+5))', 720),
            ('log(10)', 2.302585092994046),
            ('mod(7*2, 3) + 4', 6),
            ('pow((mod(sqrt(5*5) + mod(44, 55) * mod( pow(5, 3) , 65), 3 * mod(88, 77)) + 4), 2) + x', 86),
            ("(7*9+2) * log(4+8 * sqrt(64) )", 274.26800083644696),
            ("(8+5) + (3*7 + mod(5,2))", 35),
        ]

        for formula, expected_result in formulas:
            with self.subTest(formula=formula, expected_result=expected_result):
                unknown_dict = {'x': 5}
                result = compute_formula(formula, unknown_dict)
                self.assertEqual(result, expected_result)

        # Test sqrt of negative number - should return error message
        sqrt_negative_formula = '(8+6*8) + sqrt(mod(7*2+(x+5), 3) + 4 - 50) + sqrt((8*7+5)+7)'
        unknown_dict = {'x': 5}
        result = compute_formula(sqrt_negative_formula, unknown_dict)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("Can't sqrt"))

    def test_peculiar_formulas_with_random_values(self):
        """Test complex nested formulas with random variable values."""

        for _ in range(100):
            x = random.uniform(-100, 100)

            formulas = [
                (
                    "sqrt( sqrt(7*7) + sin(cos(12/6) + tan(PI/4)) + (abs(x)*9+2) * log(4+8 * sqrt(64))) + (7*(3+2 / (8-6)) - floor(sqrt(PI*abs(x)*5))) + tan(PI/4) + 2*PI",
                    (math.sqrt(math.sqrt(7*7) + math.sin(math.cos(12/6) + math.tan(math.pi/4)) +
                     (math.fabs(x)*9+2) * math.log(4+8 * math.sqrt(64))) +
                     (7*(3+2 / (8-6)) - math.floor(math.sqrt(math.pi*math.fabs(x)*5))) +
                     math.tan(math.pi/4) + 2*math.pi)
                ),
                ('factorial(ceil(sin(x)+5))', math.factorial(math.ceil(math.sin(x) + 5))),
                ('mod(x*2, 3) + 4', math.fmod(x * 2, 3) + 4),
                (
                    'pow((mod(sqrt(5*5) + mod(x, 55) * mod( pow(5, 3) , 65), 3 * mod(88, 77)) + 4), 2) + x',
                    (math.pow((math.fmod(math.sqrt(5 * 5) + math.fmod(x, 55) * math.fmod(math.pow(5, 3), 65),
                     3 * math.fmod(88, 77)) + 4), 2) + x)
                ),
                ("(7*x+2) * log(4 * sqrt(64) )", (7 * x + 2) * math.log(4 * math.sqrt(64))),
                ("(8+5) + (x*7 + mod(x,2))", (8 + 5) + (x * 7 + math.fmod(x, 2))),
            ]

            for formula, expected_result in formulas:
                with self.subTest(formula=formula, expected_result=expected_result, x=x):
                    unknown_dict = {'x': x}
                    result = compute_formula(formula, unknown_dict)
                    self.assertEqual(result, expected_result)


if __name__ == "__main__":
    # Create a test suite with the tests from the TestCase class
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestEvaluateFormula)

    # Run the test suite
    unittest.TextTestRunner(verbosity=2).run(test_suite)
