from pathlib import Path
from math import ceil

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
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
Window.clearcolor = (1, 1, 1, 1)


class VentanaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Área superior para categorías: 2 filas + scroll horizontal
        self.contenedor_scroll = ScrollView(
            size_hint=(1, 0.8),
            do_scroll_x=True,
            do_scroll_y=False,
            scroll_type=["bars", "content"],
            bar_width=6,
        )

        self.grid_categorias = GridLayout(
            rows=2,                 # <-- 2 filas fijas
            spacing=10,
            padding=10,
            size_hint=(None, 1),    # <-- clave: NO ocupar ancho automáticamente
        )

        # <-- clave: el grid crece según su contenido => habilita scroll horizontal
        self.grid_categorias.bind(minimum_width=self.grid_categorias.setter("width"))

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

        self.grid_categorias.clear_widgets()
        self.botones_categoria = []

        for ruta in rutas:
            boton = Button(background_normal=str(ruta), size_hint=(None, None))
            self.grid_categorias.add_widget(boton)
            self.botones_categoria.append(boton)

        self._actualizar_tamano_categorias()

    def _actualizar_tamano_categorias(self, *_args):
        if not self.botones_categoria:
            return

        grid = self.grid_categorias

        # padding (l,t,r,b)
        pad = grid.padding
        pad_x = (pad[0] + pad[2]) if isinstance(pad, (list, tuple)) and len(pad) == 4 else (pad[0] * 2 if isinstance(pad, (list, tuple)) else pad * 2)
        pad_y = (pad[1] + pad[3]) if isinstance(pad, (list, tuple)) and len(pad) == 4 else (pad[1] * 2 if isinstance(pad, (list, tuple)) else pad * 2)

        sp = grid.spacing
        spacing_x = sp[0] if isinstance(sp, (list, tuple)) else sp
        spacing_y = sp[1] if isinstance(sp, (list, tuple)) else sp

        h = max(1, self.contenedor_scroll.height)
        alto_disponible = max(1, h - pad_y - spacing_y)  # 2 filas => 1 hueco vertical
        btn = alto_disponible / 2

        # fuerza celdas cuadradas
        grid.row_force_default = True
        grid.col_force_default = True
        grid.row_default_height = btn
        grid.col_default_width = btn

        for b in self.botones_categoria:
            b.size = (btn, btn)

        # opcional (pero ayuda): fija columnas para que NUNCA cree 3 filas
        grid.cols = ceil(len(self.botones_categoria) / 2)

        # ancho total => scroll horizontal
        cols = grid.cols
        grid.width = pad_x + cols * btn + max(0, cols - 1) * spacing_x


class PyTEAApp(App):
    def build(self):
        return VentanaPrincipal()


if __name__ == "__main__":
    PyTEAApp().run()
