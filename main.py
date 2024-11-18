from kivy.config import Config

# Fijar el tamaño de la ventana
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

from src.ventana_principal import PyTEAApp

if __name__ == "__main__":
    PyTEAApp().run()
