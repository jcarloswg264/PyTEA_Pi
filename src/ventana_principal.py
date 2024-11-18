from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config

# Configuración inicial de tamaño de ventana
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', True)

class VentanaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Área de pictogramas seleccionables
        self.area_pictogramas = Label(
            text="Pictogramas seleccionables",
            size_hint=(1, 0.8),
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1)  # Texto blanco
        )
        self.area_pictogramas.bind(size=self.area_pictogramas.setter('text_size'))
        self.add_widget(self.area_pictogramas)

        # Barra inferior
        barra_inferior = BoxLayout(size_hint=(1, 0.2), spacing=10, padding=10)

        # Botón de inicio (alineado a la izquierda)
        boton_inicio = Button(
            text="",
            background_normal='assets/inicio.png',
            background_down='assets/inicio.png',
            size_hint=(None, None),
            size=(80, 80),
            background_color=(1, 1, 1, 1)  # Fondo blanco
        )
        barra_inferior.add_widget(boton_inicio)

        # Área central para pictogramas seleccionados
        area_seleccionados = Label(
            text="Seleccionados",
            size_hint=(1, 1),
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1)  # Texto blanco
        )
        area_seleccionados.bind(size=area_seleccionados.setter('text_size'))
        barra_inferior.add_widget(area_seleccionados)

        # Botones alineados a la derecha
        botones = [
            ('assets/play.png', "Play"),
            ('assets/borrar_ultimo.png', "Borrar último"),
            ('assets/borrar_todo.png', "Borrar todo"),
        ]

        for img_path, _ in botones:
            boton = Button(
                text="",
                background_normal=img_path,
                background_down=img_path,
                size_hint=(None, None),
                size=(80, 80),
                background_color=(1, 1, 1, 1)  # Fondo blanco
            )
            barra_inferior.add_widget(boton)

        # Añadir la barra inferior
        self.add_widget(barra_inferior)

class PyTEAApp(App):
    def build(self):
        return VentanaPrincipal()

if __name__ == "__main__":
    PyTEAApp().run()
