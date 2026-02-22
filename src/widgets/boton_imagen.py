"""Widget de botón basado en imagen para Kivy."""

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class BotonImagen(ButtonBehavior, Image):
    """Botón clicable que renderiza una imagen sin el skin clásico de ``Button``.

    Se usa esta combinación de `ButtonBehavior + Image` para evitar el estilo por
    defecto del `Button` (incluyendo artefactos visuales) y garantizar que los
    pictogramas se muestren siempre como imagen pura.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # "contain" mantiene la imagen completa sin deformación ni recorte.
        self.fit_mode = "contain"
