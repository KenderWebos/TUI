import ctypes
import sys
from TUI_APP.webpageblocker.blocker import activate_block, deactivate_block, toggle_block


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


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
    if not is_admin():
        run_as_admin()
        sys.exit()

    comando = input("Escribe activar, desactivar o toggle: ").lower().strip()

    if comando == "activar":
        activate_block()

    elif comando == "desactivar":
        deactivate_block()

    elif comando == "toggle":
        toggle_block()

    else:
        print("Comando no válido")