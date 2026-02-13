from pathlib import Path
from math import ceil, floor

from kivy.app import App
from kivy.animation import Animation
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView

# Configuración inicial de la ventana
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
Config.set("graphics", "resizable", True)
Window.clearcolor = (0.96, 0.96, 0.96, 1)


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True


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

        self.frase_container = BoxLayout(size_hint=(1, 1))
        self.frase_center = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 1),
        )
        self.frase_rows = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            spacing=10,
            padding=(10, 10),
        )
        self.frase_center.add_widget(self.frase_rows)
        self.frase_container.add_widget(self.frase_center)

        self.add_widget(self.contenedor_scroll)

        self.botones_categoria = []
        self.botones_pictos = []
        self.botones_frase = []
        self.seleccionados = []
        self.widgets_seleccionados = []
        self.frase_rutas = []
        self.vista_actual = "categorias"
        self.categoria_actual = None
        self.contenedor_scroll.bind(size=self._on_scroll_size)
        self.contenedor_scroll.bind(size=lambda *_: self._reflow_frase_si_visible())

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

        # Área central para pictogramas seleccionados (miniaturas con scroll horizontal)
        area_seleccionados = BoxLayout(size_hint=(1, 1))
        self.area_seleccionados = area_seleccionados
        with self.area_seleccionados.canvas.before:
            self.flash_color = Color(1, 0, 0, 0)
            self.flash_rect = Rectangle(
                pos=self.area_seleccionados.pos,
                size=self.area_seleccionados.size,
            )
        self.area_seleccionados.bind(pos=self._update_flash_rect, size=self._update_flash_rect)

        self.scroll_seleccionados = ScrollView(
            do_scroll_x=True,
            do_scroll_y=False,
            bar_width=6,
        )
        self.layout_seleccionados = BoxLayout(
            orientation="horizontal",
            size_hint=(None, 1),
            spacing=8,
            padding=(8, 0),
        )
        self.layout_seleccionados.bind(minimum_width=self.layout_seleccionados.setter("width"))
        self.scroll_seleccionados.add_widget(self.layout_seleccionados)
        area_seleccionados.add_widget(self.scroll_seleccionados)
        barra_inferior.add_widget(area_seleccionados)

        boton_play = Button(
            background_normal="assets/play.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_play)
        boton_play.bind(on_release=lambda *_: self.on_play())

        boton_borrar_ultimo = Button(
            background_normal="assets/borrar_ultimo.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_borrar_ultimo)
        boton_borrar_ultimo.bind(on_release=lambda *_: self.borrar_ultimo())

        boton_borrar_todo = Button(
            background_normal="assets/borrar_todo.png",
            size_hint=(None, None),
            size=(80, 80),
        )
        barra_inferior.add_widget(boton_borrar_todo)
        boton_borrar_todo.bind(on_release=lambda *_: self.borrar_todo())

        self.add_widget(barra_inferior)

        self.mostrar_categorias()

    def _crear_boton(self, **kwargs):
        source = kwargs.pop("source", None)
        if source is None and "background_normal" in kwargs:
            source = kwargs.pop("background_normal")
        kwargs.pop("background_down", None)
        kwargs.pop("background_color", None)
        return ImageButton(source=source, **kwargs)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _update_rect_fondo(self, instance, value):
        self.rect_fondo.size = instance.size
        self.rect_fondo.pos = instance.pos


    def _update_flash_rect(self, instance, *_):
        self.flash_rect.pos = instance.pos
        self.flash_rect.size = instance.size

    def destello_error_seleccionados(self):
        Animation.cancel_all(self.flash_color, "a")
        self.flash_color.a = 0
        anim = Animation(a=0.35, duration=0.10) + Animation(a=0.0, duration=0.35)
        anim.start(self.flash_color)

    def on_play(self):
        if not self.seleccionados:
            self.destello_error_seleccionados()
            return
        self.mostrar_frase_seleccionados()

    def _reset_scroll_inicio(self, *_args):
        # Horizontal: izquierda
        self.contenedor_scroll.scroll_x = 0.0
        self.contenedor_scroll.scroll_y = 1.0  # por si alguna vez hay y, arriba

    def _on_scroll_size(self, *_args):
        if self.vista_actual == "categorias":
            self._actualizar_tamano_categorias()
        elif self.vista_actual == "pictos":
            self._actualizar_tamano_pictos()

    def _cargar_categorias(self):
        self.mostrar_categorias()

    def _split_counts(self, n, filas):
        base = n // filas
        extra = n % filas
        return [base + 1 if i < extra else base for i in range(filas)]

    def _calcular_btn_size_frase(self, ancho, alto, filas, n):
        spacing_x = 10
        spacing_y = 10
        padding_x = 20
        padding_y = 20
        cols = max(1, ceil(n / filas))
        btn_w = (ancho - padding_x - max(0, cols - 1) * spacing_x) / cols
        btn_h = (alto - padding_y - max(0, filas - 1) * spacing_y) / filas
        return max(1, floor(min(btn_w, btn_h)))

    def mostrar_categorias(self):
        self.vista_actual = "categorias"
        self.categoria_actual = None
        self.contenedor_scroll.do_scroll_x = True
        self.contenedor_scroll.do_scroll_y = False

        rutas = sorted(Path("pictograms/categorias").glob("*.png"))

        self.grid_categorias.clear_widgets()
        self.grid_categorias.rows = 2
        self.grid_categorias.cols = max(1, ceil(len(rutas) / 2))
        self.botones_categoria = []

        for ruta in rutas:
            categoria = ruta.stem
            boton = self._crear_boton(
                source=str(ruta),
                size_hint=(None, None),
            )
            boton.bind(on_release=lambda _btn, cat=categoria: self.mostrar_pictogramas(cat))
            self.grid_categorias.add_widget(boton)
            self.botones_categoria.append(boton)

        self.contenedor_scroll.clear_widgets()
        self.contenedor_scroll.add_widget(self.grid_categorias)
        Clock.schedule_once(self._reset_scroll_inicio, 0)
        Clock.schedule_once(self._reset_scroll_inicio, 0.01)
        self._actualizar_tamano_categorias()

    def mostrar_pictogramas(self, categoria):
        self.vista_actual = "pictos"
        self.categoria_actual = categoria
        self.contenedor_scroll.do_scroll_x = True
        self.contenedor_scroll.do_scroll_y = False

        rutas = sorted((Path("pictograms") / categoria).glob("*.png"))

        self.grid_pictos.clear_widgets()
        self.grid_pictos.rows = 2
        self.grid_pictos.cols = max(1, ceil(len(rutas) / 2))
        self.botones_pictos = []
        self.botones_frase = []

        for ruta in rutas:
            boton = self._crear_boton(
                source=str(ruta),
                size_hint=(None, None),
            )
            boton.bind(on_release=lambda _btn, p=str(ruta): self.seleccionar_picto(p))
            self.grid_pictos.add_widget(boton)
            self.botones_pictos.append(boton)

        self.contenedor_scroll.clear_widgets()
        self.contenedor_scroll.add_widget(self.grid_pictos)
        Clock.schedule_once(self._reset_scroll_inicio, 0)
        Clock.schedule_once(self._reset_scroll_inicio, 0.01)
        self._actualizar_tamano_pictos()

    def mostrar_frase_seleccionados(self, rutas=None):
        if rutas is None:
            if self.seleccionados:
                rutas = list(self.seleccionados)
            else:
                rutas = list(self.frase_rutas)
        else:
            rutas = list(rutas)

        if not rutas:
            return

        self.vista_actual = "frase"
        self.contenedor_scroll.do_scroll_x = False
        self.contenedor_scroll.do_scroll_y = False

        self.frase_rows.clear_widgets()

        ancho = max(1, self.contenedor_scroll.width)
        alto = max(1, self.contenedor_scroll.height)
        n = len(rutas)

        filas = 1
        alto_util = max(1, alto - 20)
        size1 = self._calcular_btn_size_frase(ancho, alto, 1, n)
        if size1 < 0.50 * alto_util:
            filas = 2

        size2 = self._calcular_btn_size_frase(ancho, alto, 2, n)
        if filas == 2 and size2 < 0.33 * alto_util:
            filas = 3

        btn = self._calcular_btn_size_frase(ancho, alto, filas, n)
        counts = self._split_counts(n, filas)

        spacing_x = 10
        spacing_y = 10
        padding_x = 20
        padding_y = 20

        widths = []
        idx = 0
        for count in counts:
            row = BoxLayout(
                orientation="horizontal",
                size_hint=(None, None),
                spacing=spacing_x,
            )
            for _ in range(count):
                ruta = rutas[idx]
                idx += 1
                widget = ImageButton(
                    source=ruta,
                    size_hint=(None, None),
                    size=(btn, btn),
                )
                row.add_widget(widget)

            row.width = count * btn + max(0, count - 1) * spacing_x
            row.height = btn
            widths.append(row.width)
            self.frase_rows.add_widget(row)

        max_row_w = max(widths) if widths else 0
        total_h = filas * btn + max(0, filas - 1) * spacing_y
        self.frase_rows.size = (max_row_w + padding_x, total_h + padding_y)

        self.frase_rutas = list(rutas)
        self.botones_frase = []

        self.seleccionados.clear()
        for widget in self.widgets_seleccionados:
            self.layout_seleccionados.remove_widget(widget)
        self.widgets_seleccionados.clear()
        self.scroll_seleccionados.scroll_x = 0.0

        self.contenedor_scroll.clear_widgets()
        self.contenedor_scroll.add_widget(self.frase_container)

    def _reflow_frase_si_visible(self):
        if self.vista_actual != "frase":
            return
        if not self.frase_rutas:
            return
        if self.contenedor_scroll.children and self.contenedor_scroll.children[0] is self.frase_container:
            self.mostrar_frase_seleccionados(self.frase_rutas)

    def seleccionar_picto(self, ruta_png: str):
        self.seleccionados.append(ruta_png)

        mini = Image(
            source=ruta_png,
            size_hint=(None, None),
            size=(70, 70),
            allow_stretch=True,
            keep_ratio=True,
        )
        self.layout_seleccionados.add_widget(mini)
        self.widgets_seleccionados.append(mini)

        Clock.schedule_once(self._auto_scroll_seleccionados, 0)

        # volver a categorías
        self.mostrar_categorias()

    def borrar_ultimo(self):
        if not self.seleccionados:
            return
        self.seleccionados.pop()
        widget = self.widgets_seleccionados.pop()
        self.layout_seleccionados.remove_widget(widget)
        Clock.schedule_once(self._auto_scroll_seleccionados, 0)

    def borrar_todo(self):
        self.seleccionados.clear()
        for widget in self.widgets_seleccionados:
            self.layout_seleccionados.remove_widget(widget)
        self.widgets_seleccionados.clear()
        Clock.schedule_once(self._auto_scroll_seleccionados, 0)

    def _auto_scroll_seleccionados(self, *_):
        sv = self.scroll_seleccionados
        content = self.layout_seleccionados

        # si el contenido es más ancho que el viewport, ir a la derecha
        if content.width > sv.width:
            sv.scroll_x = 1.0
        else:
            sv.scroll_x = 0.0

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
        btn_size = max(1, (h - pad_y - spacing_y) / 2)

        grid.row_force_default = True
        grid.col_force_default = True
        grid.row_default_height = btn_size
        grid.col_default_width = btn_size

        for boton in self.botones_pictos:
            boton.size = (btn_size, btn_size)

        cols = max(1, grid.cols)
        grid.width = pad_x + cols * btn_size + max(0, cols - 1) * spacing_x

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
