"""Ventana principal de PyTEA.

Arquitectura (modular):
- widgets/: piezas visuales reutilizables (`BotonImagen`, utilidades de resaltado).
- componentes/: bloques funcionales (`BarraSeleccionados`, `VistaFrase`,
  `ReproductorAudioFrase`).
- `VentanaPrincipal`: orquesta layout principal, navegación entre vistas y eventos.
"""

from math import ceil
from pathlib import Path

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from .componentes.barra_seleccionados import BarraSeleccionados
from .componentes.reproductor_audio_frase import ReproductorAudioFrase
from .componentes.vista_frase import VistaFrase
from .widgets.boton_imagen import BotonImagen
from .widgets.resaltado_borde import aplicar_resaltado_borde, limpiar_resaltado_borde

# Configuración inicial de ventana.
Config.set("kivy", "exit_on_escape", "0")
Config.set("graphics", "fullscreen", "auto")
Config.set("graphics", "borderless", "1")
Config.set("graphics", "resizable", False)
Window.clearcolor = (0.96, 0.96, 0.96, 1)


class VentanaPrincipal(BoxLayout):
    """Contenedor principal y orquestador de vistas/eventos de la app."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        Window.show_cursor = False

        # Fondo general para cubrir toda la ventana y evitar fondo negro por defecto.
        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            self.rect_fondo = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._actualizar_fondo, pos=self._actualizar_fondo)

        # ScrollView principal reutilizado para categorías y pictogramas.
        self.contenedor_scroll = ScrollView(
            size_hint=(1, 0.8),
            do_scroll_x=True,
            do_scroll_y=False,
            scroll_type=["bars", "content"],
            bar_width=6,
        )
        self.add_widget(self.contenedor_scroll)

        self.grid_categorias = GridLayout(rows=2, spacing=10, padding=10, size_hint=(None, 1))
        self.grid_categorias.bind(minimum_width=self.grid_categorias.setter("width"))

        self.grid_pictos = GridLayout(rows=2, spacing=10, padding=10, size_hint=(None, 1))
        self.grid_pictos.bind(minimum_width=self.grid_pictos.setter("width"))

        self.vista_frase = VistaFrase(size_hint=(1, 1))

        # Estado de navegación y datos temporales.
        self.botones_categoria = []
        self.botones_pictos = []
        self._frase_visible = False
        self.categoria_actual = None

        # Reproductor modular de audio + resaltado.
        self.reproductor = ReproductorAudioFrase()

        # Escuchamos cambios de tamaño para recalcular tamaños en grids y reflow de frase.
        self.contenedor_scroll.bind(size=self._al_cambiar_tamano_principal)

        self._crear_barra_inferior()
        self.mostrar_categorias()

    def _crear_barra_inferior(self):
        """Construye barra inferior (inicio, seleccionados, play y borrado)."""
        barra_inferior = BoxLayout(size_hint=(1, 0.2), padding=10, spacing=10)
        with barra_inferior.canvas.before:
            Color(1, 1, 1, 1)
            self.rect_barra = Rectangle(size=barra_inferior.size, pos=barra_inferior.pos)
        barra_inferior.bind(size=self._actualizar_rect_barra, pos=self._actualizar_rect_barra)

        boton_inicio = Button(background_normal="assets/inicio.png", size_hint=(None, None), size=(80, 80))
        boton_inicio.bind(on_release=lambda *_: self.mostrar_categorias())
        barra_inferior.add_widget(boton_inicio)

        self.area_seleccionados = BoxLayout(size_hint=(1, 1))
        with self.area_seleccionados.canvas.before:
            self.flash_color = Color(1, 0, 0, 0)
            self.flash_rect = Rectangle(pos=self.area_seleccionados.pos, size=self.area_seleccionados.size)
        self.area_seleccionados.bind(pos=self._actualizar_flash_rect, size=self._actualizar_flash_rect)

        self.barra_seleccionados = BarraSeleccionados(size_hint=(1, 1))
        self.area_seleccionados.add_widget(self.barra_seleccionados)
        barra_inferior.add_widget(self.area_seleccionados)

        boton_play = Button(background_normal="assets/play.png", size_hint=(None, None), size=(80, 80))
        boton_play.bind(on_release=lambda *_: self.on_play())
        barra_inferior.add_widget(boton_play)

        boton_borrar_ultimo = Button(
            background_normal="assets/borrar_ultimo.png", size_hint=(None, None), size=(80, 80)
        )
        boton_borrar_ultimo.bind(on_release=lambda *_: self.barra_seleccionados.borrar_ultimo())
        barra_inferior.add_widget(boton_borrar_ultimo)

        boton_borrar_todo = Button(
            background_normal="assets/borrar_todo.png", size_hint=(None, None), size=(80, 80)
        )
        boton_borrar_todo.bind(on_release=lambda *_: self.barra_seleccionados.borrar_todo())
        barra_inferior.add_widget(boton_borrar_todo)

        self.add_widget(barra_inferior)

    def on_play(self):
        """Gestiona botón PLAY según vista actual."""
        if self._frase_visible:
            if not self.vista_frase.obtener_rutas():
                self.destello_error_seleccionados()
                return
            # PLAY en frase visible: reiniciar reproducción desde el principio.
            self.reproductor.reiniciar()
            return

        if self.barra_seleccionados.esta_vacia():
            self.destello_error_seleccionados()
            return

        rutas = self.barra_seleccionados.obtener_rutas()
        self.vista_frase.establecer_frase(rutas)
        self.vista_frase.refluir(self.contenedor_scroll.width, self.contenedor_scroll.height)

        self.contenedor_scroll.do_scroll_x = False
        self.contenedor_scroll.do_scroll_y = False
        self.contenedor_scroll.clear_widgets()
        self.contenedor_scroll.add_widget(self.vista_frase)

        self._frase_visible = True

        # Al pasar a frase, se vacía el buffer visual/interno de seleccionados.
        self.barra_seleccionados.borrar_todo()

        self.reproductor.reproducir(self.vista_frase.obtener_rutas(), self.vista_frase.obtener_widgets())

    def mostrar_categorias(self):
        """Muestra categorías (2 filas + scroll horizontal) y limpia estado de frase."""
        self._detener_y_limpiar_frase()

        self.categoria_actual = None
        self.contenedor_scroll.do_scroll_x = True
        self.contenedor_scroll.do_scroll_y = False

        rutas = sorted(Path("pictograms/categorias").glob("*.png"))

        # Orden defensivo para evitar GridLayoutException al reutilizar grid.
        self.grid_categorias.clear_widgets()
        self.grid_categorias.rows = 2
        self.grid_categorias.cols = max(1, ceil(len(rutas) / 2))
        self.botones_categoria = []

        for ruta in rutas:
            boton = BotonImagen(source=str(ruta), size_hint=(None, None))
            boton.bind(on_release=lambda _b, cat=ruta.stem: self.mostrar_pictogramas(cat))
            self.grid_categorias.add_widget(boton)
            self.botones_categoria.append(boton)

        self.contenedor_scroll.clear_widgets()
        self.contenedor_scroll.add_widget(self.grid_categorias)

        # schedule_once doble: asegura reset tras medición/layout del frame actual.
        Clock.schedule_once(self._reset_scroll_inicio, 0)
        Clock.schedule_once(self._reset_scroll_inicio, 0.01)

        self._actualizar_tamano_grid_dos_filas(self.grid_categorias, self.botones_categoria)

    def mostrar_pictogramas(self, categoria: str):
        """Muestra pictogramas de categoría en 2 filas con scroll horizontal."""
        self._frase_visible = False
        self.categoria_actual = categoria

        self.contenedor_scroll.do_scroll_x = True
        self.contenedor_scroll.do_scroll_y = False

        rutas = sorted((Path("pictograms") / categoria).glob("*.png"))

        # Orden defensivo para evitar GridLayoutException al reutilizar grid.
        self.grid_pictos.clear_widgets()
        self.grid_pictos.rows = 2
        self.grid_pictos.cols = max(1, ceil(len(rutas) / 2))
        self.botones_pictos = []

        for ruta in rutas:
            boton = BotonImagen(source=str(ruta), size_hint=(None, None))
            boton.bind(on_release=lambda _b, p=str(ruta): self.seleccionar_picto(p))
            self.grid_pictos.add_widget(boton)
            self.botones_pictos.append(boton)

        self.contenedor_scroll.clear_widgets()
        self.contenedor_scroll.add_widget(self.grid_pictos)

        Clock.schedule_once(self._reset_scroll_inicio, 0)
        Clock.schedule_once(self._reset_scroll_inicio, 0.01)

        self._actualizar_tamano_grid_dos_filas(self.grid_pictos, self.botones_pictos)

    def seleccionar_picto(self, ruta_png: str):
        """Añade selección a barra inferior y vuelve a categorías."""
        self.barra_seleccionados.agregar(ruta_png)
        self.mostrar_categorias()

    def destello_error_seleccionados(self):
        """Destello rojo suave sobre área de seleccionados cuando falta contenido."""
        Animation.cancel_all(self.flash_color, "a")
        self.flash_color.a = 0
        anim = Animation(a=0.35, duration=0.10) + Animation(a=0.0, duration=0.35)
        anim.start(self.flash_color)

    def _detener_y_limpiar_frase(self):
        """Sale de modo frase: detiene audio, limpia estado y resaltados."""
        self.reproductor.detener()
        self._frase_visible = False

    def _actualizar_tamano_grid_dos_filas(self, grid: GridLayout, botones: list):
        """Ajusta botones cuadrados y ancho total de un GridLayout de 2 filas.

        - Tamaño del botón se calcula con la altura disponible del `ScrollView`.
        - El ancho total se fija manualmente para habilitar scroll horizontal real.
        """
        if not botones:
            return

        pad_x, pad_y = self._descomponer_padding(grid.padding)
        sep_x, sep_y = self._descomponer_spacing(grid.spacing)

        alto_scroll = max(1, self.contenedor_scroll.height)
        tam_boton = max(1, (alto_scroll - pad_y - sep_y) / 2)

        grid.row_force_default = True
        grid.col_force_default = True
        grid.row_default_height = tam_boton
        grid.col_default_width = tam_boton

        for boton in botones:
            boton.size = (tam_boton, tam_boton)

        grid.cols = max(1, ceil(len(botones) / 2))
        grid.width = pad_x + grid.cols * tam_boton + max(0, grid.cols - 1) * sep_x

    def _al_cambiar_tamano_principal(self, *_):
        """Reacciona al resize para mantener tamaños consistentes."""
        if self._frase_visible and self.contenedor_scroll.children:
            if self.contenedor_scroll.children[0] is self.vista_frase:
                self.vista_frase.refluir(self.contenedor_scroll.width, self.contenedor_scroll.height)
                # Si hay audio en curso, tras reflow hay nuevos widgets visuales,
                # por eso actualizamos referencias para resaltado sincronizado.
                self.reproductor.actualizar_widgets(self.vista_frase.obtener_widgets())
                return

        if self.contenedor_scroll.children and self.contenedor_scroll.children[0] is self.grid_categorias:
            self._actualizar_tamano_grid_dos_filas(self.grid_categorias, self.botones_categoria)
        elif self.contenedor_scroll.children and self.contenedor_scroll.children[0] is self.grid_pictos:
            self._actualizar_tamano_grid_dos_filas(self.grid_pictos, self.botones_pictos)

    def _reset_scroll_inicio(self, *_):
        """Fuerza scroll principal al inicio (izquierda)."""
        self.contenedor_scroll.scroll_x = 0.0
        self.contenedor_scroll.scroll_y = 1.0

    def _actualizar_fondo(self, instancia, _valor):
        self.rect_fondo.size = instancia.size
        self.rect_fondo.pos = instancia.pos

    def _actualizar_rect_barra(self, instancia, _valor):
        self.rect_barra.size = instancia.size
        self.rect_barra.pos = instancia.pos

    def _actualizar_flash_rect(self, instancia, *_):
        self.flash_rect.pos = instancia.pos
        self.flash_rect.size = instancia.size

    def _descomponer_padding(self, padding):
        """Normaliza padding Kivy en suma horizontal/vertical."""
        if isinstance(padding, (list, tuple)):
            if len(padding) == 4:
                return padding[0] + padding[2], padding[1] + padding[3]
            if len(padding) == 2:
                return padding[0] * 2, padding[1] * 2
            if len(padding) == 1:
                return padding[0] * 2, padding[0] * 2
        return padding * 2, padding * 2

    def _descomponer_spacing(self, spacing):
        """Normaliza spacing Kivy en componente X e Y."""
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
