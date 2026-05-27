from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Input, Button, Static


class CalculatorApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #container {
        width: 50;
        height: auto;
        border: round cyan;
        padding: 1 2;
    }

    Input {
        margin-bottom: 1;
    }

    Button {
        margin-top: 1;
    }

    #result {
        margin-top: 2;
        height: 3;
        content-align: center middle;
        border: solid green;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="container"):
            yield Input(placeholder="Primer numero", id="num1")
            yield Input(placeholder="Segundo numero", id="num2")

            yield Button("Sumar", id="add")
            yield Button("Restar", id="sub")
            yield Button("Multiplicar", id="mul")
            yield Button("Dividir", id="div")

            yield Static("Resultado aparecerá aquí", id="result")

        yield Footer()

    def calculate(self, operation: str):
        num1 = self.query_one("#num1", Input).value
        num2 = self.query_one("#num2", Input).value
        result_widget = self.query_one("#result", Static)

        try:
            a = float(num1)
            b = float(num2)

            if operation == "add":
                result = a + b
            elif operation == "sub":
                result = a - b
            elif operation == "mul":
                result = a * b
            elif operation == "div":
                if b == 0:
                    result_widget.update("No se puede dividir por cero")
                    return
                result = a / b

            result_widget.update(f"Resultado: {result}")

        except ValueError:
            result_widget.update("Ingresa numeros validos")

    def on_button_pressed(self, event: Button.Pressed):
        self.calculate(event.button.id)


if __name__ == "__main__":
    CalculatorApp().run()