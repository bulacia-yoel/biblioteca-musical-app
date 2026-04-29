"""
Modelo de datos de la biblioteca musical.

Este archivo contiene la lista enlazada que guarda las canciones
y los métodos para guardar y cargar información usando JSON.
"""

import json
import os


class SongNode:
    """Nodo que representa una canción individual en la lista enlazada."""

    def __init__(self, title, artist, file_path):
        """
        Inicializa una canción.

        Args:
            title (str): Título de la canción.
            artist (str): Nombre del artista.
            file_path (str): Ruta del archivo de audio.
        """
        self.title = title
        self.artist = artist
        self.file_path = file_path
        self.next_node = None


class MusicLibrary:
    """Lista enlazada que gestiona la colección de canciones."""

    def __init__(self):
        """Inicializa la biblioteca musical vacía."""
        self.head = None

    def add_song(self, title, artist, file_path):
        """
        Añade una nueva canción al final de la lista enlazada.

        Args:
            title (str): Título de la canción.
            artist (str): Nombre del artista.
            file_path (str): Ruta del archivo de audio.
        """
        new_song = SongNode(title, artist, file_path)

        if not self.head:
            self.head = new_song
            return

        current = self.head

        while current.next_node:
            current = current.next_node

        current.next_node = new_song

    def delete_song_by_index(self, index):
        """
        Elimina una canción usando su posición en la lista.

        Args:
            index (int): Posición de la canción que se desea eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no se pudo.
        """
        if self.head is None:
            return False

        if index < 0:
            return False

        if index == 0:
            self.head = self.head.next_node
            return True

        current = self.head
        previous = None
        current_index = 0

        while current:
            if current_index == index:
                previous.next_node = current.next_node
                return True

            previous = current
            current = current.next_node
            current_index += 1

        return False

    def get_all_songs(self):
        """
        Recorre la lista y devuelve una lista de diccionarios.

        Returns:
            list: Lista de canciones en formato diccionario.
        """
        songs_list = []
        current = self.head

        while current:
            songs_list.append({
                "title": current.title,
                "artist": current.artist,
                "file_path": current.file_path
            })
            current = current.next_node

        return songs_list

    def clear_library(self):
        """Vacía la lista enlazada en la RAM."""
        self.head = None

    def save_to_json(self, filepath):
        """
        Guarda las canciones en un archivo JSON.

        Args:
            filepath (str): Ruta del archivo JSON.
        """
        songs_list = self.get_all_songs()

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(songs_list, file, indent=4)

    def load_from_json(self, filepath):
        """
        Carga canciones desde un archivo JSON.

        Args:
            filepath (str): Ruta del archivo JSON.
        """
        if not os.path.exists(filepath):
            return

        self.clear_library()

        with open(filepath, 'r', encoding='utf-8') as file:
            try:
                songs_data = json.load(file)

                for item in songs_data:
                    title = item.get('title', '').strip()
                    artist = item.get('artist', '').strip()
                    file_path = item.get('file_path', '').strip()

                    if title != "" and artist != "":
                        self.add_song(title, artist, file_path)

            except json.JSONDecodeError:
                pass


if __name__ == '__main__':
    library = MusicLibrary()
    test_file = 'songs_data.json'

    print("1. Añadiendo canciones a la RAM...")
    library.add_song(
        "Yellow",
        "Coldplay",
        "assets/music/yellow.mp3"
    )
    library.add_song(
        "Bohemian Rhapsody",
        "Queen",
        "assets/music/bohemian_rhapsody.mp3"
    )

    print("   Estado de la RAM:", library.get_all_songs())

    print("\n2. Guardando información en el disco duro...")
    library.save_to_json(test_file)
    print("   Archivo 'songs_data.json' actualizado con éxito.")

    print("\n3. Cargando desde disco...")
    library.clear_library()
    library.load_from_json(test_file)
    print("   Estado de la RAM:", library.get_all_songs())