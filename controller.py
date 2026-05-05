"""
Controlador principal de la aplicación.

Este archivo conecta la interfaz gráfica con la lógica de la biblioteca musical.
"""

import json
import os

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from models import MusicLibrary, Playlist


class MusicLibraryController:
    """Controlador que maneja las acciones principales de la aplicación."""

    def __init__(self, root_widget):
        """Recibe la interfaz principal cargada desde el archivo .kv."""
        self.root = root_widget

        self.library = MusicLibrary()
        self.playlist = Playlist()
        self.selected_song_indices = []
        self.playlist_name = "sin nombre"

        self.base_path = os.path.dirname(__file__)

        self.songs_file = os.path.join(
            self.base_path,
            "data",
            "songs_data.json"
        )

        self.playlist_file = os.path.join(
            self.base_path,
            "data",
            "playlist_data.json"
        )

        self.playlist_meta_file = os.path.join(
            self.base_path,
            "data",
            "playlist_meta.json"
        )

        self.title_input = None
        self.artist_input = None
        self.duration_input = None
        self.search_input = None
        self.playlist_name_input = None

        self.library_list = None
        self.playlist_available_list = None
        self.playlist_list = None

        self.library_status_label = None
        self.add_status_label = None
        self.playlist_status_label = None
        self.playlist_title_label = None

        self.search_button = None
        self.clear_search_button = None
        self.show_all_button = None
        self.go_add_button = None
        self.go_playlist_button = None
        self.save_song_button = None
        self.back_from_add_button = None
        self.back_from_playlist_button = None
        self.create_playlist_button = None
        self.clear_selection_button = None
        self.delete_playlist_button = None

    def start(self):
        """Inicia el controlador."""
        self.connect_widgets()
        self.connect_events()

        self.load_library_from_disk()
        self.load_playlist_from_disk()
        self.load_playlist_meta()

        self.refresh_library_list()
        self.refresh_playlist_available_list()
        self.refresh_playlist_list()
        self.refresh_playlist_title()

        self.set_status("Biblioteca cargada correctamente.")

    def connect_widgets(self):
        """Obtiene los widgets desde el archivo .kv."""
        self.title_input = self.root.ids.title_input
        self.artist_input = self.root.ids.artist_input
        self.duration_input = self.root.ids.duration_input
        self.search_input = self.root.ids.search_input
        self.playlist_name_input = self.root.ids.playlist_name_input

        self.library_list = self.root.ids.library_list
        self.playlist_available_list = self.root.ids.playlist_available_list
        self.playlist_list = self.root.ids.playlist_list

        self.library_status_label = self.root.ids.library_status_label
        self.add_status_label = self.root.ids.add_status_label
        self.playlist_status_label = self.root.ids.playlist_status_label
        self.playlist_title_label = self.root.ids.playlist_title_label

        self.search_button = self.root.ids.search_button
        self.clear_search_button = self.root.ids.clear_search_button
        self.show_all_button = self.root.ids.show_all_button
        self.go_add_button = self.root.ids.go_add_button
        self.go_playlist_button = self.root.ids.go_playlist_button
        self.save_song_button = self.root.ids.save_song_button
        self.back_from_add_button = self.root.ids.back_from_add_button
        self.back_from_playlist_button = self.root.ids.back_from_playlist_button
        self.create_playlist_button = self.root.ids.create_playlist_button
        self.clear_selection_button = self.root.ids.clear_selection_button
        self.delete_playlist_button = self.root.ids.delete_playlist_button

    def connect_events(self):
        """Conecta los botones con sus acciones."""
        self.search_button.bind(on_press=self.on_search_button_pressed)
        self.clear_search_button.bind(on_press=self.on_clear_search_button_pressed)
        self.show_all_button.bind(on_press=self.on_show_all_button_pressed)

        self.go_add_button.bind(on_press=self.go_to_add_screen)
        self.go_playlist_button.bind(on_press=self.go_to_playlist_screen)

        self.save_song_button.bind(on_press=self.on_save_song_button_pressed)
        self.back_from_add_button.bind(on_press=self.go_to_library_screen)
        self.back_from_playlist_button.bind(on_press=self.go_to_library_screen)

        self.create_playlist_button.bind(
            on_press=self.on_create_playlist_button_pressed
        )
        self.clear_selection_button.bind(
            on_press=self.on_clear_selection_button_pressed
        )
        self.delete_playlist_button.bind(
            on_press=self.on_delete_playlist_button_pressed
        )

    def go_to_library_screen(self, instance=None):
        """Muestra la pantalla principal de biblioteca."""
        self.root.current = "library_screen"
        self.refresh_library_list()
        self.set_status("Mostrando biblioteca.")

    def go_to_add_screen(self, instance=None):
        """Muestra la pantalla para añadir canciones."""
        self.clear_song_inputs()
        self.root.current = "add_screen"
        self.add_status_label.text = "Estado: esperando datos"

    def go_to_playlist_screen(self, instance=None):
        """Muestra la pantalla de playlist."""
        self.root.current = "playlist_screen"
        self.refresh_playlist_available_list()
        self.refresh_playlist_list()
        self.refresh_playlist_title()
        self.playlist_status_label.text = "Estado: listo"

    def on_save_song_button_pressed(self, instance):
        """Añade una canción nueva a la biblioteca."""
        titulo = self.title_input.text.strip()
        artista = self.artist_input.text.strip()
        duracion = self.duration_input.text.strip()

        if titulo == "" or artista == "" or duracion == "":
            self.add_status_label.text = (
                "Estado: complete título, artista y duración."
            )
            return

        self.library.add_song(titulo, artista, duracion)

        self.save_library_to_disk()
        self.refresh_library_list()
        self.refresh_playlist_available_list()
        self.clear_song_inputs()

        self.add_status_label.text = "Estado: canción guardada correctamente."
        self.set_status("Canción añadida correctamente.")
        self.root.current = "library_screen"

    def on_search_button_pressed(self, instance):
        """Busca canciones por título o artista."""
        search_text = self.search_input.text.strip()

        if search_text == "":
            self.set_status("Ingrese un texto para buscar.")
            return

        results = self.get_search_results_with_real_index(search_text)
        self.refresh_library_list(results)

        if len(results) == 0:
            self.set_status("No se encontraron canciones.")
        else:
            self.set_status(f"Se encontraron {len(results)} resultado(s).")

    def on_clear_search_button_pressed(self, instance):
        """Limpia la búsqueda y muestra toda la biblioteca."""
        self.search_input.text = ""
        self.refresh_library_list()
        self.set_status("Mostrando todas las canciones.")

    def on_show_all_button_pressed(self, instance):
        """Muestra toda la biblioteca en una ventana."""
        self.search_input.text = ""
        self.refresh_library_list()
        self.show_library_popup()
        self.set_status("Mostrando biblioteca completa.")

    def delete_song(self, index):
        """Elimina una canción de la biblioteca por posición."""
        was_deleted = self.library.delete_song_by_index(index)

        if was_deleted:
            self.selected_song_indices = []
            self.save_library_to_disk()
            self.search_input.text = ""

            self.refresh_library_list()
            self.refresh_playlist_available_list()

            self.set_status("Canción eliminada correctamente.")
        else:
            self.set_status("No se pudo eliminar la canción.")

    def toggle_select_song(self, index):
        """Selecciona o quita una canción para la playlist."""
        song = self.library.get_song_by_index(index)

        if song is None:
            self.playlist_status_label.text = "Estado: no se pudo seleccionar."
            return

        if index in self.selected_song_indices:
            self.selected_song_indices.remove(index)
            self.refresh_playlist_available_list()
            self.playlist_status_label.text = (
                f"Estado: canción quitada: {song['titulo']}."
            )
            return

        self.selected_song_indices.append(index)
        self.refresh_playlist_available_list()

        self.playlist_status_label.text = (
            f"Estado: canción seleccionada: {song['titulo']} "
            f"({len(self.selected_song_indices)} seleccionada/s)."
        )

    def on_create_playlist_button_pressed(self, instance):
        """Crea una nueva playlist como lista enlazada."""
        if len(self.selected_song_indices) == 0:
            self.playlist_status_label.text = (
                "Estado: seleccione al menos una canción."
            )
            return

        playlist_name = self.playlist_name_input.text.strip()

        if playlist_name == "":
            playlist_name = "Mi Playlist"

        self.playlist.clear_library()

        for index in self.selected_song_indices:
            song = self.library.get_song_by_index(index)

            if song is not None:
                self.playlist.add_song_from_data(song)

        self.playlist_name = playlist_name
        self.selected_song_indices = []

        self.save_playlist_to_disk()
        self.save_playlist_meta()

        self.refresh_playlist_available_list()
        self.refresh_playlist_list()
        self.refresh_playlist_title()

        self.playlist_status_label.text = "Estado: playlist creada correctamente."

    def on_clear_selection_button_pressed(self, instance):
        """Limpia las canciones seleccionadas."""
        self.selected_song_indices = []
        self.refresh_playlist_available_list()
        self.playlist_status_label.text = "Estado: selección limpiada."

    def on_delete_playlist_button_pressed(self, instance):
        """Elimina la playlist actual."""
        self.playlist.clear_library()
        self.selected_song_indices = []
        self.playlist_name = "sin nombre"
        self.playlist_name_input.text = ""

        self.save_playlist_to_disk()
        self.save_playlist_meta()

        self.refresh_playlist_available_list()
        self.refresh_playlist_list()
        self.refresh_playlist_title()

        self.playlist_status_label.text = "Estado: playlist eliminada."

    def show_library_popup(self):
        """Muestra todas las canciones en una ventana emergente."""
        songs = self.library.get_all_songs()

        if len(songs) == 0:
            text = "La biblioteca está vacía."
        else:
            lines = []

            for index, song in enumerate(songs, start=1):
                lines.append(
                    f"{index}. {song['titulo']} - "
                    f"{song['artista']} "
                    f"({song['duracion']})"
                )

            text = "\n".join(lines)

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )

        scroll = ScrollView()

        label = Label(
            text=text,
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        label.bind(
            width=lambda instance, value: setattr(
                instance,
                "text_size",
                (value, None)
            )
        )

        label.bind(
            texture_size=lambda instance, value: setattr(
                instance,
                "height",
                value[1]
            )
        )

        scroll.add_widget(label)

        close_button = Button(
            text="Cerrar",
            size_hint_y=None,
            height=dp(40)
        )

        layout.add_widget(scroll)
        layout.add_widget(close_button)

        popup = Popup(
            title="Biblioteca completa",
            content=layout,
            size_hint=(0.85, 0.85)
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def get_search_results_with_real_index(self, search_text):
        """Busca canciones manteniendo su índice real."""
        results = []
        songs = self.library.get_all_songs()
        text = search_text.lower().strip()

        for index, song in enumerate(songs):
            titulo = song["titulo"].lower()
            artista = song["artista"].lower()

            if text in titulo or text in artista:
                results.append({
                    "song": song,
                    "index": index
                })

        return results

    def load_library_from_disk(self):
        """Carga la biblioteca desde JSON."""
        self.library.load_from_json(self.songs_file)

    def load_playlist_from_disk(self):
        """Carga la playlist desde JSON."""
        self.playlist.load_from_json(self.playlist_file)

    def load_playlist_meta(self):
        """Carga el nombre de la playlist."""
        if not os.path.exists(self.playlist_meta_file):
            return

        try:
            with open(self.playlist_meta_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.playlist_name = data.get("nombre", "sin nombre")
        except json.JSONDecodeError:
            self.playlist_name = "sin nombre"

    def save_library_to_disk(self):
        """Guarda la biblioteca en JSON."""
        os.makedirs(os.path.dirname(self.songs_file), exist_ok=True)
        self.library.save_to_json(self.songs_file)

    def save_playlist_to_disk(self):
        """Guarda la playlist en JSON."""
        os.makedirs(os.path.dirname(self.playlist_file), exist_ok=True)
        self.playlist.save_to_json(self.playlist_file)

    def save_playlist_meta(self):
        """Guarda el nombre de la playlist."""
        os.makedirs(os.path.dirname(self.playlist_meta_file), exist_ok=True)

        data = {
            "nombre": self.playlist_name
        }

        with open(self.playlist_meta_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def refresh_library_list(self, songs=None):
        """Actualiza la lista visual de la biblioteca."""
        if songs is None:
            items = [
                {
                    "song": song,
                    "index": index
                }
                for index, song in enumerate(self.library.get_all_songs())
            ]
        else:
            items = songs

        self.library_list.data = [
            {
                "titulo": item["song"]["titulo"],
                "artista": item["song"]["artista"],
                "duracion": item["song"]["duracion"],
                "index": item["index"]
            }
            for item in items
        ]

        self.library_list.refresh_from_data()

    def refresh_playlist_available_list(self):
        """Actualiza las canciones disponibles para seleccionar."""
        songs = self.library.get_all_songs()

        self.playlist_available_list.data = [
            {
                "titulo": song["titulo"],
                "artista": song["artista"],
                "duracion": song["duracion"],
                "index": index,
                "selected": index in self.selected_song_indices
            }
            for index, song in enumerate(songs)
        ]

        self.playlist_available_list.refresh_from_data()

    def refresh_playlist_list(self):
        """Actualiza la lista visual de la playlist."""
        songs = self.playlist.get_all_songs()

        self.playlist_list.data = [
            {
                "titulo": song["titulo"],
                "artista": song["artista"],
                "duracion": song["duracion"]
            }
            for song in songs
        ]

        self.playlist_list.refresh_from_data()

    def refresh_playlist_title(self):
        """Actualiza el título visible de la playlist."""
        self.playlist_title_label.text = "Playlist: " + self.playlist_name

    def clear_song_inputs(self):
        """Limpia los campos del formulario."""
        self.title_input.text = ""
        self.artist_input.text = ""
        self.duration_input.text = ""

    def set_status(self, message):
        """Muestra un mensaje en la pantalla principal."""
        self.library_status_label.text = "Estado: " + message
