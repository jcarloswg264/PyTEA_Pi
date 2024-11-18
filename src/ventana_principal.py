from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class PyTEAApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Zona de pictogramas
        pictograms_area = BoxLayout()
        pictograms_area.add_widget(Button(text="Pictograma 1"))
        pictograms_area.add_widget(Button(text="Pictograma 2"))

        # Barra inferior
        bottom_bar = BoxLayout(size_hint_y=0.2)
        bottom_bar.add_widget(Button(text="Inicio"))
        bottom_bar.add_widget(Button(text="Play"))
        bottom_bar.add_widget(Button(text="Borrar Último"))
        bottom_bar.add_widget(Button(text="Borrar Todo"))

        # Añadir todo al layout principal
        layout.add_widget(pictograms_area)
        layout.add_widget(bottom_bar)

        return layout
