from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.lang import Builder

# Configuración inicial de la ventana
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
Config.set("graphics", "resizable", True)

class VentanaPrincipal(BoxLayout):
    pass


class PyTEAApp(App):
    def build(self):
        return Builder.load_file("src/ventana_principal.kv")


if __name__ == "__main__":
    PyTEAApp().run()
