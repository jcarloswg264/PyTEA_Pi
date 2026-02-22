import sys

from kivy.config import Config
from kivy.core.window import Window

modo_kiosko = "-k" in sys.argv

if modo_kiosko:
    Config.set("kivy", "exit_on_escape", "0")
    Config.set("graphics", "fullscreen", "auto")
    Config.set("graphics", "borderless", "1")
    Config.set("graphics", "resizable", False)
    Window.show_cursor = False
else:
    Config.set("graphics", "width", "800")
    Config.set("graphics", "height", "480")
    Config.set("graphics", "resizable", True)

from src.ventana_principal import PyTEAApp

if __name__ == "__main__":
    PyTEAApp().run()
