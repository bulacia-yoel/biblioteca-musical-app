"""
Controlador principal de la aplicación.

Este archivo conecta la interfaz gráfica con la lógica de la biblioteca musical.
"""

import os

from kivy.core.audio import SoundLoader

from models import MusicLibrary


class MusicLibraryController:
    """Controlador que manejará las acciones principales de la interfaz."""

    def __init__(self, root_widget):
        """
        Recibe el widget principal cargado desde el archivo .kv.

        Args:
            root_widget: Widget principal cargado desde Kivy.
        """
        self.root = root_widget
        self.library = MusicLibrary()
        self.current_sound = None

        # Archivo donde se guardarán las canciones
        self.data_file = os.path.join(
            os.path.dirname(__file__),
            'songs_data.json'
        )

        # Carpeta base del proyecto
        self.base_path = os.path.dirname(__file__)

        # Referencias a los elementos de la interfaz
        self.title_input = None
        self.artist_input = None
        self.file_path_input = None
        self.add_button = None
        self.stop_button = None
        self.song_list = None

    def start(self):
        """Inicia el controlador principal."""
        print("Controlador iniciado correctamente", flush=True)

        self.connect_widgets()
        self.connect_events()
        self.load_songs_from_disk()
        self.refresh_song_list()

    def connect_widgets(self):
        """Obtiene los elementos visuales usando sus ids del archivo .kv."""
        self.title_input = self.root.ids.title_input
        self.artist_input = self.root.ids.artist_input
        self.file_path_input = self.root.ids.file_path_input
        self.add_button = self.root.ids.add_button
        self.stop_button = self.root.ids.stop_button
        self.song_list = self.root.ids.song_list

    def connect_events(self):
        """Conecta los eventos de los botones con métodos del controlador."""
        self.add_button.bind(on_press=self.on_add_button_pressed)
        self.stop_button.bind(on_press=self.on_stop_button_pressed)

    def on_add_button_pressed(self, instance):
        """
        Agrega una canción cuando se presiona el botón Add Song.

        Args:
            instance: Botón que ejecutó el evento.
        """
        title = self.title_input.text.strip()
        artist = self.artist_input.text.strip()
        file_path = self.file_path_input.text.strip()

        if title == "" or artist == "" or file_path == "":
            print(
                "Error: debe completar título, artista y ruta del audio.",
                flush=True
            )
            return

        self.library.add_song(title, artist, file_path)
        self.refresh_song_list()
        self.save_songs_to_disk()
        self.clear_inputs()

        print(
            "Canción agregada y guardada correctamente:",
            title,
            "-",
            artist,
            flush=True
        )

    def delete_song(self, index):
        """
        Elimina una canción de la biblioteca usando su posición.

        Args:
            index (int): Posición de la canción en la lista.
        """
        was_deleted = self.library.delete_song_by_index(index)

        if was_deleted:
            self.refresh_song_list()
            self.save_songs_to_disk()
            print("Canción eliminada correctamente.", flush=True)
        else:
            print("No se pudo eliminar la canción.", flush=True)

    def play_song(self, file_path):
        """
        Reproduce una canción usando la ruta del archivo de audio.

        Args:
            file_path (str): Ruta del archivo de audio.
        """
        audio_path = self.get_absolute_audio_path(file_path)

        if not os.path.exists(audio_path):
            print("Error: el archivo de audio no existe.", flush=True)
            print("Ruta buscada:", audio_path, flush=True)
            return

        self.stop_current_song()

        self.current_sound = SoundLoader.load(audio_path)

        if self.current_sound is None:
            print("Error: no se pudo cargar el archivo de audio.", flush=True)
            return

        self.current_sound.play()
        print("Reproduciendo:", audio_path, flush=True)

    def on_stop_button_pressed(self, instance):
        """
        Detiene la canción actual cuando se presiona el botón Stop.

        Args:
            instance: Botón que ejecutó el evento.
        """
        self.stop_current_song()

    def stop_current_song(self):
        """Detiene la canción que se está reproduciendo actualmente."""
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None
            print("Reproducción detenida.", flush=True)

    def get_absolute_audio_path(self, file_path):
        """
        Convierte una ruta relativa en una ruta absoluta.

        Args:
            file_path (str): Ruta escrita por el usuario.

        Returns:
            str: Ruta absoluta del archivo.
        """
        if os.path.isabs(file_path):
            return file_path

        return os.path.join(self.base_path, file_path)

    def load_songs_from_disk(self):
        """Carga las canciones guardadas en el archivo JSON."""
        self.library.load_from_json(self.data_file)
        print("Canciones cargadas desde el disco.", flush=True)

    def save_songs_to_disk(self):
        """Guarda las canciones actuales en el archivo JSON."""
        self.library.save_to_json(self.data_file)
        print("Canciones guardadas automáticamente.", flush=True)

    def refresh_song_list(self):
        """Actualiza visualmente la lista de canciones."""
        songs = self.library.get_all_songs()

        self.song_list.data = [
            {
                "title": song["title"],
                "artist": song["artist"],
                "file_path": song["file_path"],
                "index": index
            }
            for index, song in enumerate(songs)
        ]

        self.song_list.refresh_from_data()

    def clear_inputs(self):
        """Limpia los campos de texto después de agregar una canción."""
        self.title_input.text = ""
        self.artist_input.text = ""
        self.file_path_input.text = ""