from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from TUI_APP.screens import DashboardScreen, LogsScreen

class tui_app(App):
    CSS_PATH = "styles.css"  # opcional

    def compose(self) -> ComposeResult:
        yield Header()
        yield DashboardScreen()
        yield Footer()

    def on_mount(self) -> None:
        self.current_screen = "dashboard"

    def switch_screen(self, screen_name: str):
        """Cambiar de pantalla"""
        if screen_name == "dashboard":
            self.push_screen(DashboardScreen())
            self.current_screen = "dashboard"
        elif screen_name == "logs":
            self.push_screen(LogsScreen())
            self.current_screen = "logs"