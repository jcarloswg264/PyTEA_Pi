from pathlib import Path
from math import ceil

from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

# Configuración inicial de la ventana
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
Config.set("graphics", "resizable", True)


class VentanaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Área superior para categorías en 2 filas con scroll horizontal.
        self.contenedor_scroll = ScrollView(
            size_hint=(1, 0.8),
            do_scroll_x=True,
            do_scroll_y=False,
            scroll_type=["bars", "content"],
            bar_width=6,
        )
        self.columnas_categorias = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            spacing=10,
            padding=10,
        )
        self.contenedor_scroll.add_widget(self.columnas_categorias)
        self.add_widget(self.contenedor_scroll)

        self.botones_categoria = []
        self.columnas = []
        self.contenedor_scroll.bind(size=self._actualizar_tamano_categorias)
        self.bind(size=self._actualizar_tamano_categorias)
        self._cargar_categorias()
        Clock.schedule_once(self._actualizar_tamano_categorias, 0)

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
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_inicio)

        # Área central para pictogramas seleccionados
        area_seleccionados = BoxLayout(size_hint=(1, 1))
        label_seleccionados = Label(
            text="Seleccionados",
            size_hint=(1, 1),
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),  # Texto negro
        )
        label_seleccionados.bind(size=label_seleccionados.setter("text_size"))
        area_seleccionados.add_widget(label_seleccionados)
        barra_inferior.add_widget(area_seleccionados)

        # Botón "Play"
        boton_play = Button(
            background_normal="assets/play.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_play)

        # Botón "Borrar último"
        boton_borrar_ultimo = Button(
            background_normal="assets/borrar_ultimo.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_borrar_ultimo)

        # Botón "Borrar todo"
        boton_borrar_todo = Button(
            background_normal="assets/borrar_todo.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_borrar_todo)

        # Añadir la barra inferior al layout principal
        self.add_widget(barra_inferior)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _cargar_categorias(self):
        """Carga todos los pictogramas en columnas de 2 filas con scroll horizontal."""
        categorias_dir = Path("pictograms/categorias")
        rutas = sorted(categorias_dir.glob("*.png"))

        # Crear una columna por cada par de categorías (2 filas fijas por columna).
        total_columnas = ceil(len(rutas) / 2)
        for _ in range(total_columnas):
            columna = BoxLayout(
                orientation="vertical",
                size_hint=(None, None),
                spacing=10,
            )
            self.columnas_categorias.add_widget(columna)
            self.columnas.append(columna)

        for indice, ruta in enumerate(rutas):
            boton = Button(
                background_normal=str(ruta),
                size_hint=(None, None),
            )
            self.columnas[indice // 2].add_widget(boton)
            self.botones_categoria.append(boton)

        self._actualizar_tamano_categorias()

    def _actualizar_tamano_categorias(self, *_args):
        if not self.botones_categoria:
            return

        padding_h = self.columnas_categorias.padding[0] * 2
        padding_v = self.columnas_categorias.padding[1] * 2
        espacio_h = self.columnas_categorias.spacing
        espacio_v = self.columnas[0].spacing if self.columnas else 10

        alto_contenedor = self.contenedor_scroll.height
        if alto_contenedor <= 1:
            return

        alto_disponible = max(1, alto_contenedor - padding_v - espacio_v)
        tamano_boton = int(alto_disponible / 2)

        # Tamaño uniforme de botones y columnas para forzar 2 filas visuales.
        for boton in self.botones_categoria:
            boton.size = (tamano_boton, tamano_boton)

        altura_columna = (tamano_boton * 2) + espacio_v
        for columna in self.columnas:
            columna.width = tamano_boton
            columna.height = altura_columna

        columnas = len(self.columnas)
        ancho_total = padding_h + columnas * tamano_boton + max(0, columnas - 1) * espacio_h
        self.columnas_categorias.width = ancho_total
        self.columnas_categorias.height = alto_contenedor


class PyTEAApp(App):
    def build(self):
        return VentanaPrincipal()


if __name__ == "__main__":
    PyTEAApp().run()
