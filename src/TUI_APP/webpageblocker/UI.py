import customtkinter as ctk
import ctypes
import sys

from TUI_APP.webpageblocker.blocker import (
    BLOCKED_SITES,
    load_config,
    activate_block,
    deactivate_block
)


class FocusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TDAH Focus - Blocked Sites Manager")
        self.geometry("450x500")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.is_active = load_config()

        self.title_label = ctk.CTkLabel(
            self,
            text="TDAH FOCUS",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=(25, 5))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Bloqueador de sitios distractores",
            font=("Arial", 14)
        )
        self.subtitle_label.pack(pady=(0, 20))

        self.status_label = ctk.CTkLabel(
            self,
            text=self.get_status_text(),
            font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=(0, 15))

        self.sites_label = ctk.CTkLabel(
            self,
            text="Sitios bloqueados:",
            font=("Arial", 12, "bold")
        )
        self.sites_label.pack(pady=(5, 5))

        self.text_area = ctk.CTkTextbox(
            self,
            width=400,
            height=210
        )
        self.text_area.pack(pady=10)

        self.text_area.insert("0.0", "\n".join(BLOCKED_SITES))
        self.text_area.configure(state="disabled")

        self.toggle_button = ctk.CTkButton(
            self,
            text=self.get_button_text(),
            command=self.toggle_filter,
            font=("Arial", 16, "bold"),
            height=60
        )
        self.toggle_button.pack(pady=25, padx=25, fill="x")

        self.update_ui()

    def get_button_text(self):
        if self.is_active:
            return "🔴 DESACTIVAR FILTRO"
        return "🟢 ACTIVAR FILTRO"

    def get_status_text(self):
        if self.is_active:
            return "Estado: FILTRO ACTIVADO"
        return "Estado: FILTRO DESACTIVADO"

    def update_ui(self):
        self.is_active = load_config()

        self.toggle_button.configure(text=self.get_button_text())
        self.status_label.configure(text=self.get_status_text())

        if self.is_active:
            self.toggle_button.configure(
                fg_color="#A52A2A",
                hover_color="#8B0000"
            )
            self.status_label.configure(text_color="#ff6666")
        else:
            self.toggle_button.configure(
                fg_color="green",
                hover_color="#006400"
            )
            self.status_label.configure(text_color="#66ff66")

    def toggle_filter(self):
        if self.is_active:
            deactivate_block()
        else:
            activate_block()

        self.update_ui()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        " ".join(sys.argv),
        None,
        1
    )


if __name__ == "__main__":
    if is_admin():
        app = FocusApp()
        app.mainloop()
    else:
        run_as_admin()