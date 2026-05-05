"""
Pruebas unitarias para el modelo de la biblioteca musical.

Estas pruebas verifican la lógica principal de la lista enlazada,
sin depender de la interfaz gráfica de Kivy.
"""

import json

from models import MusicLibrary, Playlist, SongNode


def test_song_node_has_data_and_next_pointer():
    """Verifica que el nodo tenga datos y puntero siguiente."""
    node = SongNode("Yellow", "Coldplay", "4:29")

    assert node.datos["titulo"] == "Yellow"
    assert node.datos["artista"] == "Coldplay"
    assert node.datos["duracion"] == "4:29"
    assert node.siguiente is None


def test_add_song_to_empty_library():
    """Verifica que se pueda añadir una canción a una biblioteca vacía."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")

    songs = library.get_all_songs()

    assert len(songs) == 1
    assert songs[0]["titulo"] == "Yellow"
    assert songs[0]["artista"] == "Coldplay"
    assert songs[0]["duracion"] == "4:29"


def test_add_multiple_songs():
    """Verifica que se puedan añadir varias canciones."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")
    library.add_song("Bohemian Rhapsody", "Queen", "5:55")

    songs = library.get_all_songs()

    assert len(songs) == 2
    assert songs[0]["titulo"] == "Yellow"
    assert songs[1]["titulo"] == "Bohemian Rhapsody"


def test_search_song_by_title():
    """Verifica la búsqueda por título."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")
    library.add_song("Hotel California", "Eagles", "6:30")

    results = library.search_songs("Yellow")

    assert len(results) == 1
    assert results[0]["titulo"] == "Yellow"


def test_search_song_by_artist():
    """Verifica la búsqueda por artista."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")
    library.add_song("Bohemian Rhapsody", "Queen", "5:55")

    results = library.search_songs("Queen")

    assert len(results) == 1
    assert results[0]["artista"] == "Queen"


def test_search_is_case_insensitive():
    """Verifica que la búsqueda no dependa de mayúsculas o minúsculas."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")

    results = library.search_songs("coldplay")

    assert len(results) == 1
    assert results[0]["titulo"] == "Yellow"


def test_delete_first_song():
    """Verifica que se pueda eliminar la primera canción."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")
    library.add_song("Hotel California", "Eagles", "6:30")

    deleted = library.delete_song_by_index(0)
    songs = library.get_all_songs()

    assert deleted is True
    assert len(songs) == 1
    assert songs[0]["titulo"] == "Hotel California"


def test_delete_middle_song():
    """Verifica que se pueda eliminar una canción del medio."""
    library = MusicLibrary()

    library.add_song("Song 1", "Artist 1", "3:00")
    library.add_song("Song 2", "Artist 2", "4:00")
    library.add_song("Song 3", "Artist 3", "5:00")

    deleted = library.delete_song_by_index(1)
    songs = library.get_all_songs()

    assert deleted is True
    assert len(songs) == 2
    assert songs[0]["titulo"] == "Song 1"
    assert songs[1]["titulo"] == "Song 3"


def test_delete_invalid_index():
    """Verifica que no se elimine nada con un índice inválido."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")

    deleted = library.delete_song_by_index(10)
    songs = library.get_all_songs()

    assert deleted is False
    assert len(songs) == 1


def test_get_song_by_index():
    """Verifica que se pueda obtener una canción por su índice."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")
    library.add_song("Bohemian Rhapsody", "Queen", "5:55")

    song = library.get_song_by_index(1)

    assert song is not None
    assert song["titulo"] == "Bohemian Rhapsody"


def test_get_song_by_invalid_index():
    """Verifica que un índice inválido devuelva None."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")

    song = library.get_song_by_index(5)

    assert song is None


def test_clear_library():
    """Verifica que se pueda vaciar la biblioteca."""
    library = MusicLibrary()

    library.add_song("Yellow", "Coldplay", "4:29")
    library.clear_library()

    songs = library.get_all_songs()

    assert songs == []


def test_save_and_load_json(tmp_path):
    """Verifica que la biblioteca se pueda guardar y cargar desde JSON."""
    file_path = tmp_path / "songs_data.json"

    library = MusicLibrary()
    library.add_song("Yellow", "Coldplay", "4:29")
    library.save_to_json(file_path)

    new_library = MusicLibrary()
    new_library.load_from_json(file_path)

    songs = new_library.get_all_songs()

    assert len(songs) == 1
    assert songs[0]["titulo"] == "Yellow"
    assert songs[0]["artista"] == "Coldplay"
    assert songs[0]["duracion"] == "4:29"


def test_load_json_rebuilds_linked_list(tmp_path):
    """Verifica que al cargar JSON se reconstruya la lista enlazada."""
    file_path = tmp_path / "songs_data.json"

    data = [
        {
            "titulo": "Yellow",
            "artista": "Coldplay",
            "duracion": "4:29"
        },
        {
            "titulo": "Bohemian Rhapsody",
            "artista": "Queen",
            "duracion": "5:55"
        }
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file)

    library = MusicLibrary()
    library.load_from_json(file_path)

    assert library.cabeza is not None
    assert library.cabeza.datos["titulo"] == "Yellow"
    assert library.cabeza.siguiente is not None
    assert library.cabeza.siguiente.datos["titulo"] == "Bohemian Rhapsody"


def test_playlist_add_song_from_data():
    """Verifica que la playlist pueda agregar canciones desde un diccionario."""
    playlist = Playlist()

    song_data = {
        "titulo": "Yellow",
        "artista": "Coldplay",
        "duracion": "4:29"
    }

    playlist.add_song_from_data(song_data)

    songs = playlist.get_all_songs()

    assert len(songs) == 1
    assert songs[0]["titulo"] == "Yellow"
    assert songs[0]["artista"] == "Coldplay"
    assert songs[0]["duracion"] == "4:29"
