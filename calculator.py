import sys
import math
import re
from typing import List, Union, Any

# Define constants
CONSTANTS = {
    'pi': math.pi,
    'e': math.e
}

# Define functions
FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': math.log10,
    'ln': math.log,
    'exp': math.exp,
    'abs': abs,
    'ceil': math.ceil,
    'floor': math.floor
}

def tokenize(expression: str) -> List[str]:
    """Tokenize the expression into numbers, operators, functions, and parentheses."""
    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")
        
    # Add spaces around operators and parentheses for easier splitting
    expression = re.sub(r'([+\-*/^()])', r' \1 ', expression)
    # Handle function names and constants
    for name in FUNCTIONS:
        expression = re.sub(r'\b' + re.escape(name) + r'\b', f' {name} ', expression)
    for name in CONSTANTS:
        expression = re.sub(r'\b' + re.escape(name) + r'\b', str(CONSTANTS[name]), expression)
    
    tokens = expression.split()
    # Handle negative numbers
    processed_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '-' and (i == 0 or tokens[i-1] in '(+-*/^'):
            # This is a negative sign, not a subtraction operator
            if i+1 < len(tokens):
                try:
                    # Combine with the next token if it's a number
                    num = -float(tokens[i+1])
                    processed_tokens.append(str(num))
                    i += 2  # Skip the next token as it's already processed
                    continue
                except ValueError:
                    # If next token isn't a number, treat as negative sign operator
                    processed_tokens.append(token)
            else:
                processed_tokens.append(token)
        else:
            processed_tokens.append(token)
        i += 1
    
    return processed_tokens

def parse_expression(tokens: List[str], stop_token: str = None) -> Union[float, List[Any]]:
    """Parse the tokens into a nested list structure based on precedence and parentheses."""
    if not isinstance(tokens, list):
        raise TypeError("Tokens must be a list")
        
    # We'll work with the original tokens list and modify it in place
    # Create a wrapper to handle the token consumption properly
    token_list = tokens  # Use the original reference
    
    def consume_token():
        if token_list:
            return token_list.pop(0)
        return None
    
    def peek_token():
        if token_list:
            return token_list[0]
        return None
    
    def has_tokens():
        return len(token_list) > 0
    
    def parse_primary():
        if not has_tokens():
            raise SyntaxError("Unexpected end of expression")
        token = consume_token()
        if token == '(':
            expr = parse_expression(token_list, ')')
            if not has_tokens() or consume_token() != ')':
                raise SyntaxError("Mismatched parentheses")
            return expr
        elif token in FUNCTIONS:
            if not has_tokens() or peek_token() != '(':
                raise SyntaxError(f"Function {token} must be followed by parentheses")
            consume_token()  # Remove '('
            expr = parse_expression(token_list, ')')
            if not has_tokens() or consume_token() != ')':
                raise SyntaxError("Mismatched parentheses")
            return [token, expr]
        else:
            try:
                return float(token)
            except ValueError:
                # Check if this could be an unknown function name
                if token.isalpha():
                    raise NameError(f"Unknown function: {token}")
                else:
                    raise SyntaxError(f"Invalid token: {token}")
    
    def parse_power():
        left = parse_primary()
        # Add a safety check to prevent infinite loops
        max_iterations = 1000
        iterations = 0
        while has_tokens() and peek_token() == '^' and (stop_token is None or peek_token() != stop_token) and iterations < max_iterations:
            op = consume_token()
            right = parse_primary()
            left = [op, left, right]
            iterations += 1
        if iterations >= max_iterations:
            raise ValueError("Expression too complex or infinite loop detected")
        return left
    
    def parse_term():
        left = parse_power()
        # Add a safety check to prevent infinite loops
        max_iterations = 1000
        iterations = 0
        while has_tokens() and peek_token() in '*/' and (stop_token is None or peek_token() != stop_token) and iterations < max_iterations:
            op = consume_token()
            right = parse_power()
            left = [op, left, right]
            iterations += 1
        if iterations >= max_iterations:
            raise ValueError("Expression too complex or infinite loop detected")
        return left
    
    def parse_expr():
        left = parse_term()
        # Add a safety check to prevent infinite loops
        max_iterations = 1000
        iterations = 0
        while has_tokens() and peek_token() in '+-' and (stop_token is None or peek_token() != stop_token) and iterations < max_iterations:
            op = consume_token()
            right = parse_term()
            left = [op, left, right]
            iterations += 1
        if iterations >= max_iterations:
            raise ValueError("Expression too complex or infinite loop detected")
        # Check if there are remaining tokens that should have been consumed
        if has_tokens() and (stop_token is None or peek_token() != stop_token):
            # Check if the next token is a number (indicating missing operator)
            next_token = peek_token()
            try:
                float(next_token)
                # If we can convert to float, it's a number, so there's a missing operator
                raise SyntaxError("Missing operator between operands")
            except ValueError:
                # Not a number, let it be handled by higher level parsing
                pass
        return left
    
    return parse_expr()

def evaluate_expression(parsed_expr: Union[float, List[Any], str]) -> float:
    """Evaluate the parsed expression or string expression."""
    # If input is a string, tokenize and parse it first
    if isinstance(parsed_expr, str):
        if not parsed_expr.strip():
            raise SyntaxError("Empty expression")
        tokens = tokenize(parsed_expr)
        if not tokens:
            raise SyntaxError("Empty expression")
        try:
            parsed_expr = parse_expression(tokens)
        except ValueError as e:
            # Check if this is an unknown function error
            if "Unknown function" in str(e):
                raise NameError(str(e))
            else:
                raise SyntaxError(str(e))
    
    if isinstance(parsed_expr, (int, float)):
        return float(parsed_expr)
    
    if isinstance(parsed_expr, list):
        if len(parsed_expr) == 2:  # Function call
            func_name, arg = parsed_expr
            if func_name in FUNCTIONS:
                arg_value = evaluate_expression(arg)
                try:
                    return float(FUNCTIONS[func_name](arg_value))
                except Exception as e:
                    raise ValueError(f"Error in function {func_name}: {str(e)}")
            else:
                raise NameError(f"Unknown function: {func_name}")
        elif len(parsed_expr) == 3:  # Binary operation
            op, left, right = parsed_expr
            left_val = evaluate_expression(left)
            right_val = evaluate_expression(right)
            
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                # Edge Case: Handle division by zero
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero")
                return left_val / right_val
            elif op == '^':
                # Edge Case: Handle invalid exponentiation (e.g., negative base with non-integer exponent)
                try:
                    return left_val ** right_val
                except (ValueError, OverflowError) as e:
                    raise ValueError(f"Invalid exponentiation operation: {str(e)}")
            else:
                raise ValueError(f"Unknown operator: {op}")
        else:
            raise ValueError("Invalid expression structure")
    
    raise ValueError(f"Invalid expression element: {parsed_expr}")

def calculate(expression: str) -> float:
    """Main function to calculate the result of an expression."""
    # Type checking
    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")
    
    # Edge Case: Handle empty expression
    if not expression.strip():
        raise ValueError("Empty expression")
    
    try:
        tokens = tokenize(expression)
        # Edge Case: Handle expression with no tokens
        if not tokens:
            raise ValueError("Invalid expression")
        parsed = parse_expression(tokens)
        result = evaluate_expression(parsed)
        return result
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}")

def main():
    """Main entry point for the calculator CLI."""
    if len(sys.argv) != 2:
        print("Usage: python calculator.py <expression>")
        sys.exit(1)
    
    expression = sys.argv[1]
    
    try:
        result = calculate(expression)
        # Format the result to avoid unnecessary decimal places
        if isinstance(result, float) and result.is_integer():
            print(int(result))
        else:
            print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()