import unittest
import sys
from io import StringIO
from calculator import evaluate_expression

class TestCalculator(unittest.TestCase):
    
    def test_basic_addition(self):
        self.assertEqual(evaluate_expression("1+3"), 4)
    
    def test_basic_subtraction(self):
        self.assertEqual(evaluate_expression("5-2"), 3)
    
    def test_basic_multiplication(self):
        self.assertEqual(evaluate_expression("4*3"), 12)
    
    def test_basic_division(self):
        self.assertEqual(evaluate_expression("8/2"), 4)
    
    def test_complex_expression_with_parentheses(self):
        self.assertAlmostEqual(evaluate_expression("1+(2*4+3)/3"), 3.6666666666666665)
    
    def test_exponentiation(self):
        self.assertEqual(evaluate_expression("2^3"), 8)
    
    def test_exponentiation_with_decimals(self):
        self.assertAlmostEqual(evaluate_expression("2^0.5"), 1.4142135623730951)
    
    def test_negative_numbers(self):
        self.assertEqual(evaluate_expression("-5+3"), -2)
    
    def test_sin_function(self):
        self.assertAlmostEqual(evaluate_expression("sin(0)"), 0)
    
    def test_cos_function(self):
        self.assertAlmostEqual(evaluate_expression("cos(0)"), 1)
    
    def test_sqrt_function(self):
        self.assertEqual(evaluate_expression("sqrt(16)"), 4)
    
    def test_exp_function(self):
        self.assertAlmostEqual(evaluate_expression("exp(1)"), 2.718281828459045)
    
    def test_pi_constant(self):
        self.assertAlmostEqual(evaluate_expression("pi"), 3.141592653589793)
    
    def test_e_constant(self):
        self.assertAlmostEqual(evaluate_expression("e"), 2.718281828459045)
    
    def test_complex_expression_with_functions(self):
        self.assertAlmostEqual(evaluate_expression("sin(pi/2)"), 1)
    
    def test_nested_parentheses(self):
        self.assertEqual(evaluate_expression("((2+3)*4)"), 20)
    
    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            evaluate_expression("5/0")
    
    def test_invalid_syntax_missing_operator(self):
        with self.assertRaises(SyntaxError):
            evaluate_expression("2 3")
    
    def test_invalid_syntax_unmatched_parentheses(self):
        with self.assertRaises(SyntaxError):
            evaluate_expression("(2+3")
    
    def test_invalid_function_name(self):
        with self.assertRaises(NameError):
            evaluate_expression("unknown(5)")
    
    def test_empty_expression(self):
        with self.assertRaises(SyntaxError):
            evaluate_expression("")
    
    def test_only_whitespace(self):
        with self.assertRaises(SyntaxError):
            evaluate_expression("   ")
    
    def test_multiple_decimal_points(self):
        with self.assertRaises(SyntaxError):
            evaluate_expression("2.3.4")
    
    def test_expression_with_only_operators(self):
        with self.assertRaises(SyntaxError):
            evaluate_expression("++")

if __name__ == '__main__':
    unittest.main()