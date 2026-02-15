"""Componente de barra de pictogramas seleccionados."""

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView


class BarraSeleccionados(BoxLayout):
    """Barra horizontal con miniaturas seleccionadas y estado asociado.

    Guarda tanto las rutas seleccionadas como los widgets miniatura para poder
    borrar de forma eficiente el último elemento o vaciar todo el buffer.
    """

    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self.rutas = []
        self.widgets = []

        self.scroll = ScrollView(do_scroll_x=True, do_scroll_y=False, bar_width=6)
        self.contenido = BoxLayout(
            orientation="horizontal",
            size_hint=(None, 1),
            spacing=8,
            padding=(8, 0),
        )
        # Este bind permite que el ancho del contenido crezca con sus hijos,
        # requisito para que el ScrollView pueda desplazar en horizontal.
        self.contenido.bind(minimum_width=self.contenido.setter("width"))

        self.scroll.add_widget(self.contenido)
        self.add_widget(self.scroll)

    def agregar(self, ruta_png: str) -> None:
        """Agrega una miniatura al final del buffer."""
        self.rutas.append(ruta_png)
        mini = Image(
            source=ruta_png,
            size_hint=(None, None),
            size=(70, 70),
            allow_stretch=True,
            keep_ratio=True,
        )
        self.contenido.add_widget(mini)
        self.widgets.append(mini)
        # schedule_once: esperamos al siguiente frame para que Kivy recalcule
        # tamaños antes de decidir si hay que mover el scroll al final.
        Clock.schedule_once(self._auto_scroll, 0)

    def borrar_ultimo(self) -> None:
        """Elimina el último pictograma seleccionado si existe."""
        if not self.rutas:
            return

        self.rutas.pop()
        widget = self.widgets.pop()
        self.contenido.remove_widget(widget)
        Clock.schedule_once(self._auto_scroll, 0)

    def borrar_todo(self) -> None:
        """Vacía por completo el buffer y las miniaturas."""
        self.rutas.clear()
        for widget in self.widgets:
            self.contenido.remove_widget(widget)
        self.widgets.clear()
        Clock.schedule_once(self._auto_scroll, 0)

    def esta_vacia(self) -> bool:
        """Indica si no hay elementos seleccionados."""
        return len(self.rutas) == 0

    def obtener_rutas(self) -> list[str]:
        """Devuelve copia de rutas seleccionadas en orden."""
        return list(self.rutas)

    def _auto_scroll(self, *_):
        """Ajusta el scroll: izquierda si cabe todo, derecha si desborda."""
        if self.contenido.width > self.scroll.width:
            self.scroll.scroll_x = 1.0
        else:
            self.scroll.scroll_x = 0.0
