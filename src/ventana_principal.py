from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from pathlib import Path
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from math import ceil

# Configuración inicial de la ventana
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
Config.set("graphics", "resizable", True)

class VentanaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Área superior para las categorías de pictogramas
        contenedor_scroll = ScrollView(
            size_hint=(1, 0.8),
            do_scroll_x=True,
            do_scroll_y=False,
            bar_width=6,
        )
        self.area_pictogramas = GridLayout(
            rows=2,
            spacing=10,
            padding=10,
            size_hint=(None, 1),
        )
        contenedor_scroll.add_widget(self.area_pictogramas)
        self.add_widget(contenedor_scroll)
        self.botones_categoria = []
        self.area_pictogramas.bind(size=self._actualizar_tamano_categorias)
        self._cargar_categorias()

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

    def _cargar_categorias(self):
        """Carga los pictogramas de las categorias y los agrega al layout"""
        categorias_dir = Path("pictograms/categorias")
        for ruta in sorted(categorias_dir.glob("*.png")):
            boton = Button(
                background_normal=str(ruta),
                size_hint=(None, None),
            )
            self.area_pictogramas.add_widget(boton)
            self.botones_categoria.append(boton)
        self._actualizar_tamano_categorias()

    def _actualizar_tamano_categorias(self, *_args):
        if not self.botones_categoria:
            return

        padding_horizontal = self.area_pictogramas.padding[0] * 2
        padding_vertical = self.area_pictogramas.padding[1] * 2
        espacio_vertical = self.area_pictogramas.spacing[1]
        alto_disponible = max(
            1,
            self.area_pictogramas.height - padding_vertical - espacio_vertical,
        )
        tamano_boton = alto_disponible / 2

        for boton in self.botones_categoria:
            boton.size = (tamano_boton, tamano_boton)

        columnas = ceil(len(self.botones_categoria) / 2)
        espacio_horizontal = self.area_pictogramas.spacing[0]
        ancho_total = (
            padding_horizontal
            + columnas * tamano_boton
            + max(0, columnas - 1) * espacio_horizontal
        )
        self.area_pictogramas.width = ancho_total


class PyTEAApp(App):
    def build(self):
        return VentanaPrincipal()


if __name__ == "__main__":
    PyTEAApp().run()
