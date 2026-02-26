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
        self._sonido_actual = None
        self._activo = False
        self._token = 0
        self._parada_manual = False
        # Guardamos el handler para poder hacer unbind fiable del mismo callback.
        self._handler_on_stop = None
        self._rutas = []
        self._widgets = []
        self._indice = 0
        self._widget_resaltado = None

    def detener(self) -> None:
        """Detiene reproducción y limpia resaltado/estado temporal."""
        self._activo = False
        # El token invalida callbacks antiguos que lleguen tarde.
        self._token += 1
        self._parada_manual = True
        self._limpiar_resaltado()

        if self._sonido_actual:
            if self._handler_on_stop is not None:
                try:
                    self._sonido_actual.unbind(on_stop=self._handler_on_stop)
                except Exception:
                    pass
            try:
                self._sonido_actual.stop()
            except Exception:
                pass
            self._sonido_actual = None
            self._handler_on_stop = None

        self._parada_manual = False
        self._rutas = []
        self._widgets = []
        self._indice = 0

    def reproducir(self, rutas_png: list[str], widgets: list) -> None:
        """Inicia una nueva reproducción desde el principio."""
        # Siempre partimos de estado limpio para evitar solapes de secuencias.
        self.detener()
        self._rutas = list(rutas_png)
        self._widgets = list(widgets)
        self._indice = 0
        self._activo = True
        # Token nuevo para esta ejecución; invalida on_stop de secuencias viejas.
        self._token += 1
        token = self._token
        self._reproducir_indice(token)

    def reiniciar(self) -> None:
        """Reinicia la reproducción usando la frase ya cargada."""
        if not self._rutas:
            return
        self.reproducir(self._rutas, self._widgets)

    def esta_activo(self) -> bool:
        """Indica si hay un sonido en reproducción."""
        return self._activo and self._sonido_actual is not None

    def actualizar_widgets(self, widgets: list) -> None:
        """Actualiza referencias de widgets tras un reflow de la frase."""
        self._widgets = list(widgets)

    def _reproducir_indice(self, token: int):
        if token != self._token or not self._activo:
            return

        if self._indice >= len(self._rutas):
            self._limpiar_resaltado()
            self._activo = False
            return

        png = Path(self._rutas[self._indice])
        categoria = png.parent.name
        stem = png.stem
        mp3 = Path("audio") / categoria / f"{stem}.mp3"

        if not mp3.exists():
            self._indice += 1
            self._reproducir_indice(token)
            return

        if self._sonido_actual:
            if self._handler_on_stop is not None:
                try:
                    self._sonido_actual.unbind(on_stop=self._handler_on_stop)
                except Exception:
                    pass
            # Esta parada es manual: no debe disparar avance de secuencia.
            self._parada_manual = True
            try:
                self._sonido_actual.stop()
            except Exception:
                pass
            self._parada_manual = False
            self._sonido_actual = None
            self._handler_on_stop = None

        sonido = SoundLoader.load(str(mp3))
        if not sonido:
            self._indice += 1
            self._reproducir_indice(token)
            return

        self._sonido_actual = sonido
        self._handler_on_stop = lambda *_: self._al_terminar(token)
        sonido.bind(on_stop=self._handler_on_stop)

        self._resaltar_indice(self._indice)
        sonido.play()

    def _al_terminar(self, token: int):
        if token != self._token or not self._activo:
            return
        # Si el stop fue manual (detener/reiniciar/cambio), no avanzamos.
        if self._parada_manual:
            return
        # schedule_once evita reentradas del callback de audio dentro del mismo tick.
        Clock.schedule_once(lambda _dt: self._avanzar(token), 0)

    def _avanzar(self, token: int):
        if token != self._token or not self._activo:
            return
        self._limpiar_resaltado()
        self._indice += 1
        self._reproducir_indice(token)

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
