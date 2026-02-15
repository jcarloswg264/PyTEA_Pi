"""Utilidades para dibujar/quitar resaltado de borde en widgets."""

from kivy.graphics import Color, Line


def aplicar_resaltado_borde(widget, color_rgba=(0.2, 0.6, 1, 1), grosor=3):
    """Aplica un borde al widget indicado usando ``canvas.after``.

    `canvas.after` se usa para que el borde se dibuje por encima de la imagen.
    Además se hace bind a ``pos`` y ``size`` para que el borde siga al widget
    cuando el layout lo recoloca o redimensiona.
    """
    limpiar_resaltado_borde(widget)

    with widget.canvas.after:
        widget._resaltado_color = Color(*color_rgba)
        widget._resaltado_linea = Line(
            rectangle=(widget.x, widget.y, widget.width, widget.height),
            width=grosor,
        )

    def _actualizar_borde(*_):
        if hasattr(widget, "_resaltado_linea"):
            widget._resaltado_linea.rectangle = (
                widget.x,
                widget.y,
                widget.width,
                widget.height,
            )

    widget._resaltado_callback = _actualizar_borde
    widget.bind(pos=_actualizar_borde, size=_actualizar_borde)


def limpiar_resaltado_borde(widget):
    """Elimina el borde de resaltado si existe en el widget."""
    callback = getattr(widget, "_resaltado_callback", None)
    if callback is not None:
        try:
            widget.unbind(pos=callback, size=callback)
        except Exception:
            pass

    if hasattr(widget, "_resaltado_color"):
        try:
            widget.canvas.after.remove(widget._resaltado_color)
        except Exception:
            pass
        del widget._resaltado_color

    if hasattr(widget, "_resaltado_linea"):
        try:
            widget.canvas.after.remove(widget._resaltado_linea)
        except Exception:
            pass
        del widget._resaltado_linea

    if hasattr(widget, "_resaltado_callback"):
        del widget._resaltado_callback
