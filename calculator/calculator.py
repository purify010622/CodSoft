import math
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich import box
from rich.align import Align

# Initialize Rich Console
console = Console()

class Calculator:
    def __init__(self):
        self.history = []

    def log_history(self, expression, result):
        self.history.append({"expr": expression, "res": result})
        if len(self.history) > 5:  # Keep last 5 records
            self.history.pop(0)

    def add(self, a, b): return a + b, "+"
    def subtract(self, a, b): return a - b, "-"
    def multiply(self, a, b): return a * b, "*"
    def divide(self, a, b):
        if b == 0: raise ValueError("Division by zero")
        return a / b, "/"
    def power(self, a, b): return math.pow(a, b), "^"
    def modulus(self, a, b): return a % b, "%"

    def get_history_table(self):
        table = Table(title="Recent History", box=box.SIMPLE, style="dim")
        table.add_column("Expression", style="cyan")
        table.add_column("Result", style="green bold")
        
        if not self.history:
            table.add_row("No history", "-")
        else:
            for item in self.history:
                table.add_row(item["expr"], str(item["res"]))
        return table

    def print_menu(self):
        menu_table = Table(show_header=False, box=box.ROUNDED, border_style="blue")
        menu_table.add_row("[1] Addition (+)", "[4] Division (/)")
        menu_table.add_row("[2] Subtraction (-)", "[5] Power (^)")
        menu_table.add_row("[3] Multiplication (*)", "[6] Modulus (%)")
        return menu_table

def main():
    calc = Calculator()
    
    while True:
        console.clear()
        
        # Header
        header_text = Text("PROFESSIONAL CALCULATOR", style="bold white on blue", justify="center")
        console.print(Panel(header_text, style="blue"))
        
        # Display History
        console.print(Align.center(calc.get_history_table()))
        console.print("\n")
        
        # Display Menu
        console.print(Align.center(calc.print_menu()))
        console.print(Align.center("[dim]Press [bold red]Q[/] to quit[/]"), style="dim")
        
        choice = console.input("\n[bold yellow]Select Operation (1-6) > [/]")
        
        if choice.lower() == 'q':
            console.print("[bold green]Goodbye! 🚀[/]")
            break
            
        if choice not in ['1', '2', '3', '4', '5', '6']:
            console.print("[bold red]Invalid selection![/]")
            time.sleep(1)
            continue

        try:
            console.print("[cyan]Enter first number:[/]")
            num1 = float(console.input("> "))
            console.print("[cyan]Enter second number:[/]")
            num2 = float(console.input("> "))

            result = 0
            symbol = ""
            expr_str = ""

            with console.status("[bold green]Calculating...[/]", spinner="dots"):
                time.sleep(0.5)  # Fake processing time for effect
                if choice == '1': result, symbol = calc.add(num1, num2)
                elif choice == '2': result, symbol = calc.subtract(num1, num2)
                elif choice == '3': result, symbol = calc.multiply(num1, num2)
                elif choice == '4': result, symbol = calc.divide(num1, num2)
                elif choice == '5': result, symbol = calc.power(num1, num2)
                elif choice == '6': result, symbol = calc.modulus(num1, num2)

            # Format results
            if result.is_integer():
                result = int(result)
            if num1.is_integer(): num1 = int(num1)
            if num2.is_integer(): num2 = int(num2)
            
            expr_str = f"{num1} {symbol} {num2}"
            calc.log_history(expr_str, result)
            
            # Show Result Panel
            console.print(Panel(
                Align.center(f"[bold white]{expr_str} = [/][bold green underline]{result}[/]"),
                title="Result",
                style="green",
                border_style="green"
            ))
            
        except ValueError as e:
            console.print(f"[bold red]Error: {str(e)}[/]")
        except Exception as e:
            console.print(f"[bold red]An error occurred: {str(e)}[/]")
            
        console.input("\n[dim]Press Enter to continue...[/]")

if __name__ == "__main__":
    main()
