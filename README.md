# 🎵 Biblioteca Musical Personal

Aplicación desarrollada con **Python** y **Kivy** que simula una biblioteca musical usando **listas enlazadas**.

El proyecto permite registrar canciones, buscarlas, eliminarlas y crear una playlist a partir de canciones seleccionadas de la biblioteca principal.

---

## ✨ Funcionalidades

- Añadir canciones a la biblioteca.
- Buscar canciones por título o artista.
- Eliminar canciones de la colección.
- Mostrar la biblioteca completa.
- Crear una playlist con canciones seleccionadas.
- Guardar datos en archivos JSON.
- Cargar la información al iniciar la app.
- Generar un APK para Android usando Buildozer.

---

## 🧠 Estructura del nodo

Cada canción se guarda en un nodo de lista enlazada.

```python
datos = {
    "titulo": "Nombre de la canción",
    "artista": "Nombre del artista",
    "duracion": "3:45"
}

siguiente = referencia_al_siguiente_nodo
```

El nodo contiene:

- `datos`: diccionario con título, artista y duración.
- `siguiente`: puntero al siguiente nodo de la lista.

---

## 🗂️ Estructura del proyecto

```txt
biblioteca-musical-app/
│
├── main.py
├── controller.py
├── models.py
├── buildozer.spec
├── README.md
├── .gitignore
│
├── data/
│   ├── songs_data.json
│   ├── playlist_data.json
│   └── playlist_meta.json
│
├── views/
│   └── interface.kv
│
└── tests/
    └── test_models.py
```

---

## 📌 Descripción de archivos

### `main.py`

Archivo principal de la aplicación.
Carga la interfaz y ejecuta la app.

### `controller.py`

Conecta la interfaz gráfica con la lógica del programa.
Maneja botones, pantallas, búsqueda, guardado y playlist.

### `models.py`

Contiene la lógica de estructuras de datos:

- `SongNode`
- `MusicLibrary`
- `Playlist`

Aquí se implementan las listas enlazadas.

### `views/interface.kv`

Contiene el diseño visual de la aplicación usando Kivy Language.

### `data/`

Guarda los archivos JSON de la biblioteca y la playlist.

### `tests/`

Contiene pruebas unitarias del modelo.

---

## 🚀 Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd biblioteca-musical-app
```

Crear entorno virtual:

```bash
python3 -m venv env
```

Activar entorno virtual en Linux:

```bash
source env/bin/activate
```

Activar entorno virtual en Windows:

```bash
env\Scripts\activate
```

Instalar dependencias:

```bash
pip install kivy pytest
```

---

## ▶️ Ejecutar la aplicación

```bash
python main.py
```

---

## 🧪 Ejecutar pruebas

```bash
pytest
```

Si aparece error de importación:

```bash
PYTHONPATH=. pytest
```

---

## 📱 Generar APK

Instalar Buildozer:

```bash
pip install buildozer setuptools cython==0.29.34
```

Crear configuración:

```bash
buildozer init
```

En `buildozer.spec` configurar:

```txt
title = Biblioteca Musical, package.name = bibliotecamusical, package.domain = org.yoel, source.include_exts = py,kv,json, requirements = python3,kivy, orientation = portrait, fullscreen = 0 y opcionalmente android.archs = arm64-v8a.
```

Compilar APK:

```bash
buildozer -v android debug
```

El archivo `.apk` se generará en:

```txt
bin/
```

---

## 🧩 Tecnologías utilizadas

- Python
- Kivy
- Kivy Language
- JSON
- Pytest
- Buildozer

---

## 🎯 Objetivo del proyecto

El objetivo principal es aplicar el uso de **listas enlazadas** en una aplicación visual.

La biblioteca principal funciona como una lista enlazada donde cada nodo representa una canción.

La playlist también se crea como una segunda lista enlazada independiente, formada a partir de canciones seleccionadas desde la biblioteca principal.

---

## 📖 Flujo general

```txt
Usuario abre la app
        ↓
Se cargan las canciones desde JSON
        ↓
La biblioteca se muestra en pantalla
        ↓
El usuario puede añadir, buscar o eliminar canciones
        ↓
El usuario puede seleccionar canciones
        ↓
Se crea una playlist como nueva lista enlazada
        ↓
Los datos se guardan nuevamente en JSON
```

---

## 👤 Autor

Proyecto académico desarrollado como práctica de estructuras de datos.
