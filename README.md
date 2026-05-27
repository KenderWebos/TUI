# TUI App - Terminal User Interface

Aplicación de terminal interactiva (TUI) para gestionar proyectos y servicios.

## Requisitos

- Python 3.11+
- uv (gestor de paquetes moderno)

## Instalación

### 1. Instalar `uv` (si no lo tienes)

```bash
pip install uv
```

### 2. Instalar dependencias del proyecto

```bash
uv pip install -e .
```

O para desarrollo (incluye herramientas de testing y linting):

```bash
uv pip install -e ".[dev]"
```

### 3. Ejecutar la aplicación

```bash
uv run python -m TUI_APP.main
```

O simplemente:

```bash
tui-app
```

## Estructura del Proyecto

```
TUI/
├── src/TUI_APP/
│   ├── app.py              # Aplicación principal
│   ├── main.py             # Entry point
│   ├── screens.py          # Pantallas de la UI
│   ├── config.py           # Configuración
│   ├── services.py         # Servicios (ProjectService, DockerService)
│   └── utils/              # Utilidades
├── tests/                  # Tests con pytest
├── pyproject.toml          # Configuración del proyecto (uv)
└── README.md              # Este archivo
```

## Herramientas

- **Textual** → Interfaz TUI de terminal
- **Rich** → Tablas, logs, estilos avanzados
- **Typer** → Comandos CLI
- **uv** → Gestor de paquetes y entorno
- **Pydantic** → Validación de configuración
- **Pytest** → Framework de testing
- **Ruff** → Linting y formateo rápido

## Desarrollo

### Ejecutar tests

```bash
uv run pytest
```

### Formatear código

```bash
uv run ruff check --fix .
uv run black src tests
```

### Lint

```bash
uv run ruff check src tests
```

## Próximos pasos

- [ ] Agregar persistencia con SQLite
- [ ] Integrar Docker SDK
- [ ] Expandir pantallas de la UI
- [ ] Agregar más tests
