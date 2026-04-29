from kivy.app import App
from kivy.lang import Builder
import os

class MusicLibraryApp(App):
    def build(self):
        # 1. Cargamos la vista
        view_path = os.path.join(os.path.dirname(__file__), 'views', 'interface.kv')
        root_widget = Builder.load_file(view_path)

        # 2. Inyectamos datos de prueba directamente al RecycleView (song_list)
        # Esto simula lo que hará el Controlador en la siguiente fase
        root_widget.ids.song_list.data = [
            {'title': 'Bohemian Rhapsody', 'artist': 'Queen'},
            {'title': 'Shape of You', 'artist': 'Ed Sheeran'},
            {'title': 'Hotel California', 'artist': 'Eagles'}
        ]

        return root_widget

if __name__ == '__main__':
    MusicLibraryApp().run()
