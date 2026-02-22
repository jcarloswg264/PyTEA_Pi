"""Reproductor de frase con encadenado de audios MP3 y resaltado visual."""

from pathlib import Path

from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from ..widgets.resaltado_borde import aplicar_resaltado_borde, limpiar_resaltado_borde


class ReproductorAudioFrase:
    """Gestiona reproducción secuencial de audios y resaltado de pictogramas.

    Mantiene una copia interna de rutas/widgets para poder seguir reproduciendo
    aunque el buffer de seleccionados de la barra inferior se vacíe al entrar
    en la vista frase.
    """

    def __init__(self):
        self._rutas = []
        self._widgets = []
        self._indice = 0
        self._sonido_actual = None
        self._callback_on_stop_actual = None
        self._widget_resaltado = None
        self._activo = False
        self._token = 0

    def reproducir(self, rutas_png: list[str], widgets: list) -> None:
        """Inicia una nueva reproducción desde el principio."""
        # Siempre detenemos antes de empezar una frase nueva para que no quede
        # ninguna secuencia anterior viva en paralelo.
        self.detener()

        # Token: invalida callbacks viejos que pudieran dispararse tarde.
        self._token += 1
        token = self._token

        # Snapshot defensivo para no depender de listas mutables externas.
        self._rutas = list(rutas_png)
        self._widgets = list(widgets)
        self._indice = 0
        self._activo = True
        self._limpiar_resaltado()
        self._reproducir_indice(token)

    def reiniciar(self) -> None:
        """Reinicia la reproducción usando la frase ya cargada."""
        if not self._rutas:
            return

        self._token += 1
        token = self._token
        self._activo = True
        self._indice = 0
        self._detener_sonido_actual()
        self._limpiar_resaltado()
        self._reproducir_indice(token)

    def detener(self) -> None:
        """Detiene reproducción y limpia resaltado/estado temporal."""
        self._activo = False
        # Al incrementar token invalidamos callbacks antiguos pendientes.
        self._token += 1
        self._detener_sonido_actual()
        self._indice = 0
        self._limpiar_resaltado()

    def esta_activo(self) -> bool:
        """Indica si hay un sonido en reproducción."""
        return self._activo and self._sonido_actual is not None

    def actualizar_widgets(self, widgets: list) -> None:
        """Actualiza referencias de widgets tras un reflow de la frase."""
        self._widgets = list(widgets)

    def _reproducir_indice(self, token: int, *_):
        if token != self._token or not self._activo:
            return

        if self._indice >= len(self._rutas):
            self._detener_sonido_actual()
            self._limpiar_resaltado()
            self._activo = False
            return

        self._resaltar_indice(self._indice)

        png = Path(self._rutas[self._indice])
        categoria = png.parent.name
        stem = png.stem
        mp3 = Path("audio") / categoria / f"{stem}.mp3"
        self._indice += 1

        if not mp3.exists():
            Clock.schedule_once(lambda *_: self._reproducir_indice(token), 0)
            return

        # Antes de cargar/reproducir un nuevo audio hacemos unbind+stop del
        # anterior para impedir audios fantasma o solapados.
        self._detener_sonido_actual()

        sonido = SoundLoader.load(str(mp3))
        if not sonido:
            Clock.schedule_once(lambda *_: self._reproducir_indice(token), 0)
            return

        self._sonido_actual = sonido
        self._callback_on_stop_actual = lambda *_: self._on_stop(token)
        sonido.bind(on_stop=self._callback_on_stop_actual)
        sonido.play()

    def _on_stop(self, token: int):
        # Token: si cambió la reproducción activa, ignoramos callbacks viejos.
        if token != self._token or not self._activo:
            return
        Clock.schedule_once(lambda *_: self._reproducir_indice(token), 0)

    def _detener_sonido_actual(self):
        if self._sonido_actual:
            # Unbind antes de stop para que el on_stop del sonido antiguo no
            # avance la secuencia actual por error.
            if self._callback_on_stop_actual is not None:
                try:
                    self._sonido_actual.unbind(on_stop=self._callback_on_stop_actual)
                except Exception:
                    pass
            try:
                self._sonido_actual.stop()
            except Exception:
                pass
        self._sonido_actual = None
        self._callback_on_stop_actual = None

    def _resaltar_indice(self, indice: int):
        self._limpiar_resaltado()

        if indice < 0 or indice >= len(self._widgets):
            return

        widget = self._widgets[indice]
        aplicar_resaltado_borde(widget)
        self._widget_resaltado = widget

    def _limpiar_resaltado(self):
        if self._widget_resaltado is None:
            return
        limpiar_resaltado_borde(self._widget_resaltado)
        self._widget_resaltado = None
