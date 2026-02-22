import sys

from kivy.config import Config

# Evita doble evento touch/mouse en pantallas táctiles (Raspberry Pi).
Config.set("input", "mouse", "mouse,disable_multitouch")

# Detectamos el modo de ejecución por argumento de línea de comandos.
modo_kiosko = "-k" in sys.argv

if modo_kiosko:
    # Modo kiosko: pantalla completa sin bordes y sin salida con Escape.
    Config.set("kivy", "exit_on_escape", "0")
    Config.set("graphics", "fullscreen", "1")
    Config.set("graphics", "borderless", "1")
    Config.set("graphics", "resizable", False)
else:
    # Modo normal: configuración original de ventana para desarrollo/uso estándar.
    Config.set("graphics", "width", "800")
    Config.set("graphics", "height", "480")
    Config.set("graphics", "resizable", True)

from src.ventana_principal import PyTEAApp

if __name__ == "__main__":
    PyTEAApp().run()
