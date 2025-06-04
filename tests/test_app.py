import os
import sys

# Add repository root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Prevent Kivy from parsing command line arguments
os.environ.setdefault('KIVY_NO_ARGS', '1')

from src.ventana_principal import PyTEAApp, VentanaPrincipal


def test_app_builds_root_widget(monkeypatch):
    # Patch VentanaPrincipal.__init__ to avoid heavy Kivy initialization
    monkeypatch.setattr(VentanaPrincipal, "__init__", lambda self, **kw: None)
    app = PyTEAApp()
    root = app.build()
    assert isinstance(root, VentanaPrincipal)
