# Proyecto Final – Automatización de Pruebas (UI + API)

**Alumno:** Iván Rodríguez

## Descripción

Framework de automatización de pruebas end-to-end en Python que cubre:

- **UI:** flujo de compra del sitio [SauceDemo](https://www.saucedemo.com) con **Selenium WebDriver** y el patrón **Page Object Model (POM)**.
- **API REST:** endpoints de [JSONPlaceholder](https://jsonplaceholder.typicode.com) con **requests**, validando códigos de estado, tiempos de respuesta y esquemas JSON con **jsonschema**.

El propósito es demostrar buenas prácticas de QA Automation: código modular, datos externalizados en JSON, logging centralizado, esperas explícitas, capturas de pantalla automáticas en fallos y reporte HTML.

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Lenguaje base |
| pytest | Motor de pruebas, fixtures y parametrización |
| selenium + webdriver-manager | Automatización de UI y descarga automática del driver |
| requests | Cliente HTTP para las pruebas de API |
| jsonschema | Validación de la estructura de las respuestas JSON |
| pytest-html | Reporte HTML autocontenido con capturas adjuntas |
| logging | Logger centralizado (consola + `automation.log`) |

## Estructura del proyecto

```
proyecto-final-automation-testing-ivan-rodriguez/
├── conftest.py                  # Fixtures (driver, api_client), opciones CLI y hook de capturas
├── pytest.ini                   # Configuración de pytest y reporte HTML
├── requirements.txt             # Dependencias
├── README.md
├── .gitignore
├── automation.log               # Se genera al ejecutar (log del framework)
├── data/
│   └── test_data.json           # Credenciales y datos de prueba
├── pages/                       # Capa Page Object Model
│   ├── base_page.py             # Esperas explícitas y acciones genéricas
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── utils/
│   ├── logger.py                # Logger a consola y archivo
│   ├── data_loader.py           # Lectura de JSON
│   ├── api_client.py            # Cliente HTTP con logging
│   └── schema_validator.py      # Esquemas y validación jsonschema
├── tests/
│   ├── ui/
│   │   └── test_saucedemo_ui.py     # TC1 – TC5
│   └── api/
│       └── test_api_endpoints.py    # TC-API-1 – TC-API-4
└── reports/
    ├── report.html              # Reporte generado por pytest-html
    └── screenshots/             # Capturas de pruebas fallidas
```

## Casos de prueba

### UI (SauceDemo)

| ID | Tipo | Descripción |
|---|---|---|
| TC1 | Positivo | Login exitoso con credenciales válidas |
| TC2 | Negativo | Login fallido con credenciales inválidas (valida el mensaje de error) |
| TC3 | Positivo | Ordenamiento de productos por nombre (A–Z, Z–A) y precio (menor–mayor, mayor–menor) |
| TC4 | Positivo | Agregar productos al carrito y validar el contador |
| TC5 | Positivo | Checkout completo: carrito → datos del cliente → confirmación |

### API (JSONPlaceholder)

| ID | Método | Descripción |
|---|---|---|
| TC-API-1 | GET | `/users`: status 200, tiempo de respuesta, estructura JSON |
| TC-API-2 | POST | `/posts`: status 201 y validación del cuerpo |
| TC-API-3 | PUT | `/posts/1`: status 200 y recurso actualizado |
| TC-API-4 | DELETE | `/posts/1`: status 200 y cuerpo vacío |

## Instalación

Todos los comandos parten desde la carpeta **Descargas**.

### Windows (PowerShell)

```powershell
cd $env:USERPROFILE\Downloads
cd proyecto-final-automation-testing-ivan-rodriguez

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
cd ~/Downloads/proyecto-final-automation-testing-ivan-rodriguez

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Requiere Google Chrome (o Firefox) instalado. `webdriver-manager` descarga el driver automáticamente.

### Clonar desde GitHub (opcional)

```bash
cd ~/Downloads
git clone <URL-DEL-REPOSITORIO> proyecto-final-automation-testing-ivan-rodriguez
```

## Ejecución de las pruebas

```bash
# Toda la suite (UI + API) y reporte en reports/report.html
pytest

# Solo pruebas de UI
pytest tests/ui

# Solo pruebas de API
pytest tests/api

# UI sin abrir ventana del navegador
pytest tests/ui --headless

# UI en Firefox
pytest tests/ui --browser firefox

# Por marcadores
pytest -m ui
pytest -m api

# Un test específico
pytest tests/ui/test_saucedemo_ui.py::test_tc2_login_fallido
```

## Reportes y logs

- **Reporte HTML:** se genera automáticamente en `reports/report.html` en cada ejecución (autocontenido, se abre con cualquier navegador).
- **Capturas de pantalla:** cuando un test de UI falla se guarda un PNG en `reports/screenshots/` con el nombre del test y un timestamp (`<test>_<YYYYMMDD_HHMMSS>.png`) y además queda adjunto en el reporte HTML.
- **Log:** todo se registra en consola y en `automation.log`.

## Decisiones de diseño

- **Esperas explícitas únicas:** `implicitly_wait` se deja en 0 y toda sincronización pasa por `WebDriverWait` en `BasePage`.
- **Localizadores `data-test`:** son los más estables en SauceDemo.
- **Datos externos:** credenciales, productos y datos del formulario viven en `data/test_data.json`, no en el código.
- **Sin dependencias entre tests:** cada test usa su propio navegador, lo que evita contaminación de estado.
