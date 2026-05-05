"""
Modelo de datos de la biblioteca musical.

Este archivo contiene la lógica principal del proyecto:
- Nodo de canción.
- Biblioteca musical como lista enlazada.
- Playlist como otra lista enlazada.
- Guardado y carga usando archivos JSON.
"""

import json
import os


class SongNode:
    """Nodo que representa una canción dentro de una lista enlazada."""

    def __init__(self, titulo, artista, duracion):
        """
        Crea un nodo de canción.

        El nodo cumple con la estructura solicitada:
        - datos: diccionario con titulo, artista y duracion.
        - siguiente: puntero al siguiente nodo.

        Args:
            titulo (str): Título de la canción.
            artista (str): Nombre del artista.
            duracion (str): Duración de la canción.
        """
        self.datos = {
            "titulo": titulo,
            "artista": artista,
            "duracion": duracion
        }

        self.siguiente = None


class MusicLibrary:
    """Lista enlazada principal para almacenar canciones."""

    def __init__(self):
        """Inicializa la biblioteca musical vacía."""
        self.cabeza = None

    def add_song(self, titulo, artista, duracion):
        """
        Añade una canción al final de la lista enlazada.
        """
        nuevo_nodo = SongNode(titulo, artista, duracion)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza

        while actual.siguiente is not None:
            actual = actual.siguiente

        actual.siguiente = nuevo_nodo

    def get_all_songs(self):
        """
        Devuelve todas las canciones en forma de lista de diccionarios.
        """
        canciones = []
        actual = self.cabeza

        while actual is not None:
            canciones.append(actual.datos)
            actual = actual.siguiente

        return canciones

    def search_songs(self, search_text):
        """
        Busca canciones por título o artista.
        """
        resultados = []
        actual = self.cabeza
        texto = search_text.lower().strip()

        while actual is not None:
            titulo = actual.datos["titulo"].lower()
            artista = actual.datos["artista"].lower()

            if texto in titulo or texto in artista:
                resultados.append(actual.datos)

            actual = actual.siguiente

        return resultados

    def delete_song_by_index(self, index):
        """
        Elimina una canción según su posición en la lista.
        """
        if self.cabeza is None:
            return False

        if index < 0:
            return False

        if index == 0:
            self.cabeza = self.cabeza.siguiente
            return True

        actual = self.cabeza
        anterior = None
        posicion = 0

        while actual is not None:
            if posicion == index:
                anterior.siguiente = actual.siguiente
                return True

            anterior = actual
            actual = actual.siguiente
            posicion += 1

        return False

    def get_song_by_index(self, index):
        """
        Obtiene una canción según su posición.
        """
        actual = self.cabeza
        posicion = 0

        while actual is not None:
            if posicion == index:
                return actual.datos

            actual = actual.siguiente
            posicion += 1

        return None

    def clear_library(self):
        """Vacía completamente la lista enlazada."""
        self.cabeza = None

    def print_library(self):
        """
        Imprime todas las canciones en la terminal.
        """
        canciones = self.get_all_songs()

        if len(canciones) == 0:
            print("La biblioteca está vacía.")
            return

        print("=== Biblioteca Musical ===")

        for index, song in enumerate(canciones):
            print(
                f"{index + 1}. "
                f"{song['titulo']} - "
                f"{song['artista']} "
                f"({song['duracion']})"
            )

    def save_to_json(self, filepath):
        """
        Guarda la lista enlazada en un archivo JSON.
        """
        canciones = self.get_all_songs()

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(canciones, file, indent=4, ensure_ascii=False)

    def load_from_json(self, filepath):
        """
        Carga canciones desde un archivo JSON y reconstruye la lista enlazada.
        """
        if not os.path.exists(filepath):
            return

        self.clear_library()

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                canciones = json.load(file)

            for song in canciones:
                titulo = song.get("titulo", "").strip()
                artista = song.get("artista", "").strip()
                duracion = song.get("duracion", "").strip()

                if titulo != "" and artista != "" and duracion != "":
                    self.add_song(titulo, artista, duracion)

        except json.JSONDecodeError:
            print("Error: el archivo JSON está vacío o dañado.")


class Playlist(MusicLibrary):
    """
    Playlist creada a partir de canciones seleccionadas.

    También es una lista enlazada, por eso reutiliza los métodos
    de MusicLibrary.
    """

    def add_song_from_data(self, song_data):
        """
        Añade una canción a la playlist usando un diccionario existente.
        """
        self.add_song(
            song_data["titulo"],
            song_data["artista"],
            song_data["duracion"]
        )


if __name__ == "__main__":
    base_path = os.path.dirname(__file__)

    songs_file = os.path.join(
        base_path,
        "data",
        "songs_data.json"
    )

    playlist_file = os.path.join(
        base_path,
        "data",
        "playlist_data.json"
    )

    os.makedirs(os.path.dirname(songs_file), exist_ok=True)

    biblioteca = MusicLibrary()
    playlist = Playlist()

    print("\n1. Cargando canciones desde JSON...")
    biblioteca.load_from_json(songs_file)
    biblioteca.print_library()

    print("\n2. Añadiendo una canción de prueba...")
    biblioteca.add_song(
        "Hotel California",
        "Eagles",
        "6:30"
    )
    biblioteca.print_library()

    print("\n3. Buscando canciones por artista o título...")
    resultados = biblioteca.search_songs("Queen")

    if len(resultados) == 0:
        print("No se encontraron canciones.")
    else:
        print("Resultados encontrados:")

        for song in resultados:
            print(
                f"- {song['titulo']} - "
                f"{song['artista']} "
                f"({song['duracion']})"
            )

    print("\n4. Creando una playlist con canciones seleccionadas...")
    primera_cancion = biblioteca.get_song_by_index(0)
    segunda_cancion = biblioteca.get_song_by_index(1)

    if primera_cancion is not None:
        playlist.add_song_from_data(primera_cancion)

    if segunda_cancion is not None:
        playlist.add_song_from_data(segunda_cancion)

    print("Playlist creada:")
    playlist.print_library()

    print("\n5. Guardando biblioteca y playlist...")
    biblioteca.save_to_json(songs_file)
    playlist.save_to_json(playlist_file)

    print("Datos guardados correctamente.")
