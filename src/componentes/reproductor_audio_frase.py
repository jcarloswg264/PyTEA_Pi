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
        self._rutas_actuales = []
        self._widgets_actuales = []
        self._indice = 0
        self._sonido_actual = None
        self._callback_on_stop_actual = None
        self._widget_resaltado = None
        self._token_reproduccion = 0

    def reproducir(self, rutas_png: list[str], widgets: list) -> None:
        """Inicia una nueva reproducción desde el principio."""
        # Cortamos cualquier reproducción previa para garantizar un único sonido activo.
        self.detener()
        # Tomamos una foto fija (snapshot) de rutas/widgets para evitar
        # desincronización si la UI muta mientras se reproduce audio.
        self._rutas_actuales = list(rutas_png)[:]
        self._widgets_actuales = list(widgets)[:]
        self._indice = 0
        self._token_reproduccion += 1
        self._limpiar_resaltado()
        self._reproducir_siguiente(self._token_reproduccion)

    def reiniciar(self) -> None:
        """Reinicia la reproducción usando la frase ya cargada."""
        if not self._rutas_actuales:
            return
        self._indice = 0
        self._token_reproduccion += 1
        self._limpiar_resaltado()
        self._reproducir_siguiente(self._token_reproduccion)

    def detener(self) -> None:
        """Detiene reproducción y limpia resaltado/estado temporal."""
        self._token_reproduccion += 1
        self._detener_sonido_actual()
        self._indice = 0
        self._limpiar_resaltado()
        self._rutas_actuales = []
        self._widgets_actuales = []

    def esta_activo(self) -> bool:
        """Indica si hay un sonido en reproducción."""
        return self._sonido_actual is not None

    def actualizar_widgets(self, widgets: list) -> None:
        """Actualiza referencias de widgets tras un reflow de la frase."""
        # También copiamos aquí para no depender de referencias mutables externas.
        self._widgets_actuales = list(widgets)[:]

    def _reproducir_siguiente(self, token: int, *_):
        if token != self._token_reproduccion:
            return

        if self._indice >= len(self._rutas_actuales):
            self._sonido_actual = None
            self._limpiar_resaltado()
            return

        self._resaltar_indice(self._indice)

        png = Path(self._rutas_actuales[self._indice])
        categoria = png.parent.name
        stem = png.stem
        mp3 = Path("audio") / categoria / f"{stem}.mp3"
        self._indice += 1

        if not mp3.exists():
            Clock.schedule_once(lambda *_: self._reproducir_siguiente(token), 0)
            return

        sonido = SoundLoader.load(str(mp3))
        if not sonido:
            Clock.schedule_once(lambda *_: self._reproducir_siguiente(token), 0)
            return

        # Defensa extra: antes de iniciar un nuevo mp3, detenemos/desvinculamos
        # cualquier sonido anterior para impedir dos locuciones en paralelo.
        self._detener_sonido_actual()
        self._sonido_actual = sonido

        def _al_terminar(*_):
            # Token: evita que callbacks antiguos avancen reproducciones nuevas.
            if token != self._token_reproduccion:
                return
            Clock.schedule_once(lambda *_: self._reproducir_siguiente(token), 0)

        self._callback_on_stop_actual = _al_terminar
        sonido.bind(on_stop=_al_terminar)
        sonido.play()

    def _detener_sonido_actual(self):
        if self._sonido_actual:
            # Primero desvinculamos callback viejo para que stop() no dispare avances
            # de cadenas anteriores y no queden reproducciones cruzadas.
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

        if indice < 0 or indice >= len(self._widgets_actuales):
            return

        widget = self._widgets_actuales[indice]
        aplicar_resaltado_borde(widget)
        self._widget_resaltado = widget

    def _limpiar_resaltado(self):
        if self._widget_resaltado is None:
            return
        limpiar_resaltado_borde(self._widget_resaltado)
        self._widget_resaltado = None
