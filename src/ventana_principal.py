from pathlib import Path
from math import ceil
import unicodedata

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
Window.clearcolor = (0.96, 0.96, 0.96, 1)


class VentanaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Fondo gris claro moderno
        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            self.rect_fondo = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect_fondo, pos=self._update_rect_fondo)

        # Área principal reutilizada: categorías o pictogramas
        self.contenedor_scroll = ScrollView(
            size_hint=(1, 0.8),
            do_scroll_x=True,
            do_scroll_y=False,
            scroll_type=["bars", "content"],
            bar_width=6,
        )

        self.grid_categorias = GridLayout(
            rows=2,
            spacing=10,
            padding=10,
            size_hint=(None, 1),
        )
        self.grid_categorias.bind(minimum_width=self.grid_categorias.setter("width"))

        self.grid_pictos = GridLayout(
            rows=2,
            spacing=10,
            padding=10,
            size_hint=(None, 1),
        )
        self.grid_pictos.bind(minimum_width=self.grid_pictos.setter("width"))

        self.add_widget(self.contenedor_scroll)

        self.botones_categoria = []
        self.botones_pictos = []
        self.vista_actual = "categorias"
        self.categoria_actual = None
        self.contenedor_scroll.bind(size=self._on_scroll_size)

        # Barra inferior (Layout con fondo blanco)
        barra_inferior = BoxLayout(size_hint=(1, 0.2), padding=10, spacing=10)
        with barra_inferior.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            barra_inferior.bind(size=self._update_rect, pos=self._update_rect)

        # Botón de inicio (vuelve a categorías)
        boton_inicio = Button(
            background_normal="assets/inicio.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        boton_inicio.bind(on_release=lambda *_: self.mostrar_categorias())
        barra_inferior.add_widget(boton_inicio)

        # Área central para pictogramas seleccionados
        area_seleccionados = BoxLayout(size_hint=(1, 1))
        label_seleccionados = Label(
            text="Seleccionados",
            size_hint=(1, 1),
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
        )
        label_seleccionados.bind(size=label_seleccionados.setter("text_size"))
        area_seleccionados.add_widget(label_seleccionados)
        barra_inferior.add_widget(area_seleccionados)

        boton_play = Button(
            background_normal="assets/play.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_play)

        boton_borrar_ultimo = Button(
            background_normal="assets/borrar_ultimo.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_borrar_ultimo)

        boton_borrar_todo = Button(
            background_normal="assets/borrar_todo.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_borrar_todo)

        self.add_widget(barra_inferior)

        self._cargar_categorias()
        self.mostrar_categorias()

    def _crear_boton(self, **kwargs):
        clase = globals().get("ShadowButton", Button)
        return clase(**kwargs)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _update_rect_fondo(self, instance, value):
        self.rect_fondo.size = instance.size
        self.rect_fondo.pos = instance.pos

    def _on_scroll_size(self, *_args):
        if self.vista_actual == "categorias":
            self._actualizar_tamano_categorias()
        else:
            self._actualizar_tamano_pictos()

    def _cargar_categorias(self):
        categorias_dir = Path("pictograms/categorias")
        rutas = sorted(categorias_dir.glob("*.png"))

        self.grid_categorias.clear_widgets()
        self.botones_categoria = []

        for ruta in rutas:
            categoria = ruta.stem
            boton = self._crear_boton(
                background_normal=str(ruta),
                size_hint=(None, None),
            )
            boton.bind(on_release=lambda _btn, cat=categoria: self.mostrar_pictogramas(cat))
            self.grid_categorias.add_widget(boton)
            self.botones_categoria.append(boton)

    def mostrar_categorias(self):
        self.vista_actual = "categorias"
        self.categoria_actual = None
        self.contenedor_scroll.do_scroll_x = True
        self.contenedor_scroll.do_scroll_y = False
        self.contenedor_scroll.clear_widgets()
        self.contenedor_scroll.add_widget(self.grid_categorias)
        self._actualizar_tamano_categorias()

    def mostrar_pictogramas(self, categoria):
        self.vista_actual = "pictos"
        self.categoria_actual = categoria
        self.contenedor_scroll.do_scroll_x = True
        self.contenedor_scroll.do_scroll_y = False
        self.contenedor_scroll.clear_widgets()
        self.contenedor_scroll.add_widget(self.grid_pictos)

        pictos_dir = self._resolver_directorio_categoria(categoria)
        rutas = sorted(pictos_dir.glob("*.png")) if pictos_dir else []

        self.grid_pictos.clear_widgets()
        self.botones_pictos = []

        for ruta in rutas:
            boton = self._crear_boton(
                background_normal=str(ruta),
                size_hint=(None, None),
            )
            self.grid_pictos.add_widget(boton)
            self.botones_pictos.append(boton)

        self._actualizar_tamano_pictos()

    def _actualizar_tamano_categorias(self):
        if not self.botones_categoria:
            return

        grid = self.grid_categorias
        pad_x, pad_y = self._descomponer_padding(grid.padding)
        spacing_x, spacing_y = self._descomponer_spacing(grid.spacing)

        h = max(1, self.contenedor_scroll.height)
        btn = max(1, (h - pad_y - spacing_y) / 2)

        grid.row_force_default = True
        grid.col_force_default = True
        grid.row_default_height = btn
        grid.col_default_width = btn

        for b in self.botones_categoria:
            b.size = (btn, btn)

        grid.cols = ceil(len(self.botones_categoria) / 2)
        cols = grid.cols
        grid.width = pad_x + cols * btn + max(0, cols - 1) * spacing_x

    def _actualizar_tamano_pictos(self):
        if not self.botones_pictos:
            return

        grid = self.grid_pictos
        pad_x, pad_y = self._descomponer_padding(grid.padding)
        spacing_x, spacing_y = self._descomponer_spacing(grid.spacing)

        h = max(1, self.contenedor_scroll.height)
        btn = max(1, (h - pad_y - spacing_y) / 2)

        grid.row_force_default = True
        grid.col_force_default = True
        grid.row_default_height = btn
        grid.col_default_width = btn

        for b in self.botones_pictos:
            b.size = (btn, btn)

        grid.cols = ceil(len(self.botones_pictos) / 2)
        cols = grid.cols
        grid.width = pad_x + cols * btn + max(0, cols - 1) * spacing_x

    def _resolver_directorio_categoria(self, categoria):
        base = Path("pictograms")
        candidata = base / categoria
        if candidata.exists():
            return candidata

        categoria_norm = self._normalizar_nombre(categoria)
        for directorio in base.iterdir():
            if directorio.is_dir() and self._normalizar_nombre(directorio.name) == categoria_norm:
                return directorio
        return None

    def _normalizar_nombre(self, texto):
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(c for c in texto if not unicodedata.combining(c))
        return texto.lower().replace(" ", "_")

    def _descomponer_padding(self, padding):
        if isinstance(padding, (list, tuple)):
            if len(padding) == 4:
                return padding[0] + padding[2], padding[1] + padding[3]
            if len(padding) == 2:
                return padding[0] * 2, padding[1] * 2
            if len(padding) == 1:
                return padding[0] * 2, padding[0] * 2
        return padding * 2, padding * 2

    def _descomponer_spacing(self, spacing):
        if isinstance(spacing, (list, tuple)):
            if len(spacing) >= 2:
                return spacing[0], spacing[1]
            if len(spacing) == 1:
                return spacing[0], spacing[0]
        return spacing, spacing


class PyTEAApp(App):
    def build(self):
        return VentanaPrincipal()


if __name__ == "__main__":
    PyTEAApp().run()
