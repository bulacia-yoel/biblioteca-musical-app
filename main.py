from kivy.app import App
from kivy.lang import Builder
import os

from controller import MusicLibraryController


class MusicLibraryApp(App):
    """Aplicación principal de la biblioteca musical."""

    def build(self):
        """
        Carga la interfaz gráfica y prepara el controlador principal.
        """
        view_path = os.path.join(
            os.path.dirname(__file__),
            'views',
            'interface.kv'
        )

        root_widget = Builder.load_file(view_path)

        self.controller = MusicLibraryController(root_widget)
        self.controller.start()

        return root_widget


if __name__ == '__main__':
    MusicLibraryApp().run()