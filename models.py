import json
import os

class SongNode:
    """Nodo que representa una canción individual en la lista enlazada."""

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.next_node = None


class MusicLibrary:
    """Lista enlazada que gestiona la colección de canciones."""

    def __init__(self):
        self.head = None

    def add_song(self, title, artist):
        """Añade una nueva canción al final de la lista enlazada."""
        new_song = SongNode(title, artist)

        # Si la lista está vacía, el nuevo nodo es la cabecera
        if not self.head:
            self.head = new_song
            return

        # Si ya hay elementos, recorremos hasta el final y lo añadimos
        current = self.head
        while current.next_node:
            current = current.next_node
        current.next_node = new_song

    def get_all_songs(self):
        """Recorre la lista y devuelve un array de diccionarios.
        Esto es útil tanto para guardar en JSON como para mostrar en la interfaz."""
        songs_list = []
        current = self.head

        while current:
            songs_list.append({
                "title": current.title,
                "artist": current.artist
            })
            current = current.next_node

        return songs_list

    def clear_library(self):
        """Vacía la lista enlazada en la RAM (útil para pruebas o reiniciar)."""
        self.head = None

    def save_to_json(self, filepath):
        """Convierte la lista enlazada a formato plano y la guarda en un JSON."""
        songs_list = self.get_all_songs()

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(songs_list, file, indent=4)

    def load_from_json(self, filepath):
        """Lee un archivo JSON, reconstruye los nodos y los carga en RAM."""
        if not os.path.exists(filepath):
            return  # Si el archivo no existe, no hacemos nada

        self.clear_library()  # Limpiamos la RAM antes de cargar datos nuevos

        with open(filepath, 'r', encoding='utf-8') as file:
            try:
                songs_data = json.load(file)
                for item in songs_data:
                    self.add_song(item['title'], item['artist'])
            except json.JSONDecodeError:
                pass  # Previene errores si el archivo JSON está vacío o corrupto


# ==========================================
# ZONA DE PRUEBAS (Solo se ejecuta en consola)
# ==========================================
if __name__ == '__main__':
    # Esta sección simula el ciclo de vida de tu app
    library = MusicLibrary()
    test_file = 'test_data.json'

    print("1. Añadiendo canciones a la RAM...")
    library.add_song("Bohemian Rhapsody", "Queen")
    library.add_song("Shape of You", "Ed Sheeran")
    print("   Estado de la RAM:", library.get_all_songs())

    print("\n2. Guardando información en el disco duro...")
    library.save_to_json(test_file)
    print("   Archivo 'test_data.json' creado con éxito.")

    print("\n3. Simulando que cerramos la aplicación (Limpiando RAM)...")
    library.clear_library()
    print("   Estado de la RAM:", library.get_all_songs())

    print("\n4. Volviendo a abrir la aplicación (Cargando desde disco)...")
    library.load_from_json(test_file)
    print("   Estado de la RAM:", library.get_all_songs())
