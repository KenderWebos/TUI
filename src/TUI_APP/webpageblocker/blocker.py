import os
import shutil
import json

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
START_MARKER = "# ---BANNED---\n"
END_MARKER = "# --- END BANNED ---\n"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "focus_config.json")

BLOCKED_SITES = [
    "instagram.com",
    "tiktok.com",
    "youtube.com",
    "x.com",
    "facebook.com"
]


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("filter_active", False)
        except Exception as e:
            print(f"Error al leer configuración: {e}")
    return False


def save_config(is_active):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"filter_active": is_active}, f, indent=2)
    except Exception as e:
        print(f"Error al guardar configuración: {e}")


def get_clean_hosts_content():
    with open(HOSTS_PATH, "r") as f:
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


def activate_block():
    try:
        shutil.copy(HOSTS_PATH, HOSTS_PATH + ".bak")

        clean_content = get_clean_hosts_content()

        with open(HOSTS_PATH, "w") as f:
            f.writelines(clean_content)
            f.write("\n" + START_MARKER)

            for site in BLOCKED_SITES:
                f.write(f"127.0.0.1 {site}\n")
                f.write(f"127.0.0.1 www.{site}\n")

            f.write(END_MARKER)

        save_config(True)
        print("Filtro ACTIVADO")

    except Exception as e:
        save_config(False)
        print(f"Error al activar: {e}")


def deactivate_block():
    try:
        clean_content = get_clean_hosts_content()

        with open(HOSTS_PATH, "w") as f:
            f.writelines(clean_content)

        save_config(False)
        print("Filtro DESACTIVADO")

    except Exception as e:
        save_config(True)
        print(f"Error al desactivar: {e}")


def toggle_block():
    is_active = load_config()

    if is_active:
        deactivate_block()
    else:
        activate_block()