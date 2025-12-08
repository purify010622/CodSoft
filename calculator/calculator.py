def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        return "Error: Division by zero is not allowed"
    return a / b

def calculator():
    """Main calculator function"""
    print("=" * 40)
    print("Simple Calculator")
    print("=" * 40)
    
    # Display operation menu
    print("\nSelect operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    
    # Get operation choice
    while True:
        choice = input("\nEnter choice (1/2/3/4): ")
        if choice in ['1', '2', '3', '4']:
            break
        print("Invalid input. Please enter 1, 2, 3, or 4.")
    
    # Get numbers from user
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            break
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
    
    # Perform calculation
    if choice == '1':
        result = add(num1, num2)
        operation = "+"
    elif choice == '2':
        result = subtract(num1, num2)
        operation = "-"
    elif choice == '3':
        result = multiply(num1, num2)
        operation = "*"
    elif choice == '4':
        result = divide(num1, num2)
        operation = "/"
    
    # Display result
    print("\n" + "=" * 40)
    print(f"{num1} {operation} {num2} = {result}")
    print("=" * 40)

if __name__ == "__main__":
    calculator()
