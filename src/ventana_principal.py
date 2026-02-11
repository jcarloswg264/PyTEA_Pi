from pathlib import Path
from math import ceil

from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

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
        self.grid_categorias = GridLayout(
            rows=2,                 # 2 filas fijas
            spacing=10,
            padding=10,
            size_hint=(None, 1),    # clave para scroll horizontal
        )
        self.contenedor_scroll.add_widget(self.grid_categorias)
        self.add_widget(self.contenedor_scroll)

        self.botones_categoria = []
        self.contenedor_scroll.bind(size=self._actualizar_tamano_categorias)
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
        categorias_dir = Path("pictograms/categorias")
        rutas = sorted(categorias_dir.glob("*.png"))

        self.botones_categoria = []
        self.grid_categorias.clear_widgets()

        for ruta in rutas:
            boton = Button(
                background_normal=str(ruta),
                size_hint=(None, None),
            )
            self.grid_categorias.add_widget(boton)
            self.botones_categoria.append(boton)

        self._actualizar_tamano_categorias()

    def _actualizar_tamano_categorias(self, *_args):
        if not self.botones_categoria:
            return

        grid = self.grid_categorias

        # padding/spacing pueden ser número o (x,y) o (l,t,r,b)
        if isinstance(grid.padding, (list, tuple)):
            if len(grid.padding) == 4:
                pad_x = grid.padding[0] + grid.padding[2]
                pad_y = grid.padding[1] + grid.padding[3]
            else:  # (x, y)
                pad_x = grid.padding[0] * 2
                pad_y = grid.padding[1] * 2
        else:
            pad_x = grid.padding * 2
            pad_y = grid.padding * 2

        if isinstance(grid.spacing, (list, tuple)):
            spacing_x = grid.spacing[0]
            spacing_y = grid.spacing[1]
        else:
            spacing_x = grid.spacing
            spacing_y = grid.spacing

        h = max(1, self.contenedor_scroll.height)

        # 2 filas => un solo espacio vertical entre filas
        alto_disponible = max(1, h - pad_y - spacing_y)
        btn_size = alto_disponible / 2

        # Forzar tamaño de celdas del grid (cuadradas)
        grid.row_force_default = True
        grid.col_force_default = True
        grid.row_default_height = btn_size
        grid.col_default_width = btn_size

        for b in self.botones_categoria:
            b.size = (btn_size, btn_size)

        # con rows=2 => columnas necesarias:
        cols = ceil(len(self.botones_categoria) / 2)

        # Ancho total para que el ScrollView pueda scrollear horizontal
        grid.width = pad_x + cols * btn_size + max(0, cols - 1) * spacing_x


class PyTEAApp(App):
    def build(self):
        return VentanaPrincipal()


if __name__ == "__main__":
    PyTEAApp().run()
