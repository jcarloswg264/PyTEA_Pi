"""Vista centrada de frase sin scroll para PLAY."""

from math import ceil, floor

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from ..widgets.boton_imagen import BotonImagen


def dividir_en_filas_equilibradas(n: int, filas: int) -> list[int]:
    """Divide `n` elementos en `filas` con reparto equilibrado.

    Las primeras filas reciben el extra cuando `n` no es divisible:
    - 22, 3 -> [8, 7, 7]
    - 9, 2 -> [5, 4]
    """
    base = n // filas
    extra = n % filas
    return [base + 1 if i < extra else base for i in range(filas)]


class VistaFrase(AnchorLayout):
    """Renderiza una frase de pictogramas centrada y sin scroll (1 a 3 filas)."""

    def __init__(self, **kwargs):
        kwargs.setdefault("size_hint", (1, 1))
        super().__init__(anchor_x="center", anchor_y="center", **kwargs)

        self.rutas = []
        self.widgets_en_orden = []

        self._spacing_x = 10
        self._spacing_y = 10
        self._padding_x = 20
        self._padding_y = 20

        self.contenedor_filas = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            spacing=self._spacing_y,
            padding=(10, 10),
        )
        self.add_widget(self.contenedor_filas)

    def establecer_frase(self, rutas: list[str]) -> None:
        """Guarda frase en orden y construye layout inicial."""
        self.rutas = list(rutas)
        self.widgets_en_orden = []
        # El reflow real se hace con tamaño disponible del contenedor principal.

    def obtener_widgets(self):
        """Devuelve widgets de la frase en el mismo orden de rutas."""
        return list(self.widgets_en_orden)

    def obtener_rutas(self):
        """Devuelve rutas de la frase en orden."""
        return list(self.rutas)

    def refluir(self, ancho: float, alto: float) -> None:
        """Recalcula filas/tamaño para que toda la frase quepa centrada."""
        self.contenedor_filas.clear_widgets()
        self.widgets_en_orden = []

        n = len(self.rutas)
        if n == 0:
            self.contenedor_filas.size = (0, 0)
            return

        filas = self._elegir_filas(ancho, alto, n)
        btn = self._calcular_tamano_boton(ancho, alto, filas, n)
        reparto = dividir_en_filas_equilibradas(n, filas)

        anchos_fila = []
        indice = 0
        for cantidad in reparto:
            fila = BoxLayout(
                orientation="horizontal",
                size_hint=(None, None),
                spacing=self._spacing_x,
            )
            # AnchorLayout por fila para centrar también filas "cortas".
            ancla_fila = AnchorLayout(anchor_x="center", anchor_y="center", size_hint=(1, None))

            for _ in range(cantidad):
                ruta = self.rutas[indice]
                indice += 1
                widget = BotonImagen(source=ruta, size_hint=(None, None), size=(btn, btn))
                fila.add_widget(widget)
                self.widgets_en_orden.append(widget)

            fila.width = cantidad * btn + max(0, cantidad - 1) * self._spacing_x
            fila.height = btn
            ancla_fila.height = btn
            ancla_fila.add_widget(fila)
            anchos_fila.append(fila.width)
            self.contenedor_filas.add_widget(ancla_fila)

        max_ancho = max(anchos_fila) if anchos_fila else 0
        alto_total = filas * btn + max(0, filas - 1) * self._spacing_y
        self.contenedor_filas.size = (max_ancho + self._padding_x, alto_total + self._padding_y)

    def _elegir_filas(self, ancho: float, alto: float, n: int) -> int:
        """Aplica criterio 1->2->3 filas según tamaño resultante."""
        filas = 1
        alto_util = max(1, alto - self._padding_y)

        tam_1 = self._calcular_tamano_boton(ancho, alto, 1, n)
        if tam_1 < 0.50 * alto_util:
            filas = 2

        tam_2 = self._calcular_tamano_boton(ancho, alto, 2, n)
        if filas == 2 and tam_2 < 0.33 * alto_util:
            filas = 3

        return filas

    def _calcular_tamano_boton(self, ancho: float, alto: float, filas: int, n: int) -> int:
        """Calcula tamaño cuadrado máximo para que el bloque entre en pantalla."""
        cols = max(1, ceil(n / filas))
        btn_w = (ancho - self._padding_x - max(0, cols - 1) * self._spacing_x) / cols
        btn_h = (alto - self._padding_y - max(0, filas - 1) * self._spacing_y) / filas
        return max(1, floor(min(btn_w, btn_h)))
