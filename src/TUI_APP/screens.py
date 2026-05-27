from textual.screen import Screen
from textual.widgets import Static

class DashboardScreen(Screen):
    def compose(self):
        yield Static("🏠 Dashboard - proyectos y estado general")

class LogsScreen(Screen):
    def compose(self):
        yield Static("📄 Logs en tiempo real")