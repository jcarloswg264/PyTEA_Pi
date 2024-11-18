from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.config import Config

# Configuración inicial de la ventana
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
Config.set("graphics", "resizable", True)

class VentanaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Área superior para los pictogramas seleccionables
        self.area_pictogramas = Label(
            text="Pictogramas seleccionables",
            size_hint=(1, 0.8),
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1)  # Texto blanco
        )
        self.area_pictogramas.bind(size=self.area_pictogramas.setter("text_size"))
        self.add_widget(self.area_pictogramas)

        # Barra inferior (Layout con fondo blanco)
        barra_inferior = BoxLayout(size_hint=(1, 0.2), padding=10, spacing=10)
        with barra_inferior.canvas.before:
            Color(1, 1, 1, 1)  # Color blanco
            self.rect = Rectangle(size=self.size, pos=self.pos)
            barra_inferior.bind(size=self._update_rect, pos=self._update_rect)

        # Botón de inicio (alineado a la izquierda)
        boton_inicio = Button(
            background_normal="assets/inicio.png",
            size_hint=(None, None),
            size=(80, 80)
        )
        barra_inferior.add_widget(boton_inicio)

        # Área central para pictogramas seleccionados
        area_seleccionados = BoxLayout(size_hint=(1, 1))
        label_seleccionados = Label(
            text="Seleccionados",
            size_hint=(1, 1),
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)  # Texto negro
        )
        label_seleccionados.bind(size=label_seleccionados.setter("text_size"))
        area_seleccionados.add_widget(label_seleccionados)
        barra_inferior.add_widget(area_seleccionados)

        # Botón "Play"
        boton_play = Button(
            background_normal="assets/play.png",
            size_hint=(None, None),
            size=(80, 80)
        )
        barra_inferior.add_widget(boton_play)

        # Botón "Borrar último"
        boton_borrar_ultimo = Button(
            background_normal="assets/borrar_ultimo.png",
            size_hint=(None, None),
            size=(80, 80)
        )
        barra_inferior.add_widget(boton_borrar_ultimo)

        # Botón "Borrar todo"
        boton_borrar_todo = Button(
            background_normal="assets/borrar_todo.png",
            size_hint=(None, None),
            size=(80, 80)
        )
        barra_inferior.add_widget(boton_borrar_todo)

        # Añadir la barra inferior al layout principal
        self.add_widget(barra_inferior)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class PyTEAApp(App):
    def build(self):
        return VentanaPrincipal()


if __name__ == "__main__":
    PyTEAApp().run()
