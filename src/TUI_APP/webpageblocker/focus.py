import customtkinter as ctk
import ctypes
import os
import shutil
import sys
import json

# Configuración de archivos y marcas
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
START_MARKER = "# ---BANNED---\n"
END_MARKER = "# --- END BANNED ---\n"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "focus_config.json")

# Lista predefinida de sitios a bloquear
BLOCKED_SITES = [
    "instagram.com",
    "tiktok.com",
    "youtube.com",
    "x.com",
    "facebook.com"
]

# bloqueador de ias 
# gemini.com
# chatgpt.com
# grok.com
# deekseek.com

class BannedApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TDAH Focus - Blocked Sites Manager")
        self.geometry("450x500")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        
        self.is_active = self.load_config()

        # Título
        self.title_label = ctk.CTkLabel(self, text="TDAH FOCUS", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=(20, 5))
        
        self.subtitle_label = ctk.CTkLabel(self, text="Sitios Bloqueados", font=("Arial", 14))
        self.subtitle_label.pack(pady=(0, 15))

        # Mostrar lista de sitios (solo lectura)
        self.sites_label = ctk.CTkLabel(self, text="Sitios en la lista:", font=("Arial", 12, "bold"))
        self.sites_label.pack(pady=(10, 5))
        
        self.text_area = ctk.CTkTextbox(self, width=400, height=200)
        self.text_area.pack(pady=10)
        self.text_area.insert("0.0", "\n".join(BLOCKED_SITES))
        self.text_area.configure(state="disabled")  # Solo lectura

        # Botón grande toggle
        self.toggle_button = ctk.CTkButton(
            self, 
            text=self.get_button_text(),
            command=self.toggle_filter,
            font=("Arial", 16, "bold"),
            height=60
        )
        self.toggle_button.pack(pady=20, padx=20, fill="both")
        self.update_button_appearance()

    def load_config(self):
        """Lee la configuración guardada o crea una nueva."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get("filter_active", False)
            except Exception as e:
                print(f"Error al leer configuración: {e}")
        return False

    def save_config(self):
        """Guarda la configuración actual."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"filter_active": self.is_active}, f, indent=2)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")

    def get_button_text(self):
        """Devuelve el texto del botón según el estado."""
        return "🔴 DESACTIVAR FILTRO" if self.is_active else "🟢 ACTIVAR FILTRO"

    def update_button_appearance(self):
        """Actualiza el color del botón según el estado."""
        if self.is_active:
            self.toggle_button.configure(fg_color="#A52A2A", hover_color="#8B0000")
        else:
            self.toggle_button.configure(fg_color="green", hover_color="#006400")
        self.toggle_button.configure(text=self.get_button_text())

    def toggle_filter(self):
        """Alterna el estado del filtro."""
        self.is_active = not self.is_active
        self.save_config()
        
        if self.is_active:
            self.activate_block()
        else:
            self.deactivate_block()
        
        self.update_button_appearance()

    def get_clean_hosts_content(self):
        """Devuelve el contenido del archivo hosts SIN la sección BANNED."""
        with open(HOSTS_PATH, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        skip = False
        for line in lines:
            if line == START_MARKER:
                skip = True
                continue
            if line == END_MARKER:
                skip = False
                continue
            if not skip:
                new_lines.append(line)
        return new_lines

    def activate_block(self):
        """Activa el bloqueo de sitios."""
        try:
            shutil.copy(HOSTS_PATH, HOSTS_PATH + ".bak")  # Backup
            clean_content = self.get_clean_hosts_content()
            
            with open(HOSTS_PATH, 'w') as f:
                f.writelines(clean_content)
                f.write("\n" + START_MARKER)
                for site in BLOCKED_SITES:
                    f.write(f"127.0.0.1 {site}\n")
                    f.write(f"127.0.0.1 www.{site}\n")
                f.write(END_MARKER)
            print("✓ Filtro ACTIVADO")
        except Exception as e:
            print(f"Error al activar: {e}")
            self.is_active = False

    def deactivate_block(self):
        """Desactiva el bloqueo de sitios."""
        try:
            clean_content = self.get_clean_hosts_content()
            with open(HOSTS_PATH, 'w') as f:
                f.writelines(clean_content)
            print("✓ Filtro DESACTIVADO")
        except Exception as e:
            print(f"Error al desactivar: {e}")
            self.is_active = True

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        app = BannedApp()
        app.mainloop()
    else:
        # Relanzar con permisos de administrador automáticamente
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)