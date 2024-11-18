from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class PyTEAApp(App):
    def build(self):
        # Crear un layout principal
        layout_principal = BoxLayout(orientation="vertical")

        # Crear una sección superior para los pictogramas seleccionables
        pictogramas_area = Label(text="Pictogramas seleccionables", size_hint=(1, 0.8))
        layout_principal.add_widget(pictogramas_area)

        # Crear la barra inferior
        barra_inferior = BoxLayout(size_hint=(1, 0.2))

        # Añadir los botones
        boton_inicio = Button(text="Inicio", size_hint=(0.2, 1))
        boton_play = Button(text="Play", size_hint=(0.2, 1))
        boton_borrar_ultimo = Button(text="Borrar último", size_hint=(0.2, 1))
        boton_borrar_todo = Button(text="Borrar todo", size_hint=(0.2, 1))

        # Área para los pictogramas seleccionados (en miniatura)
        pictogramas_seleccionados = Label(text="Seleccionados", size_hint=(0.2, 1))

        # Añadir widgets a la barra inferior
        barra_inferior.add_widget(boton_inicio)
        barra_inferior.add_widget(pictogramas_seleccionados)
        barra_inferior.add_widget(boton_play)
        barra_inferior.add_widget(boton_borrar_ultimo)
        barra_inferior.add_widget(boton_borrar_todo)

        # Añadir la barra inferior al layout principal
        layout_principal.add_widget(barra_inferior)

        return layout_principal


if __name__ == "__main__":
    PyTEAApp().run()
