# API Music Preferences App in Django

Este proyecto es una API REST construida con **Django** que permite a los usuarios gestionar sus preferencias musicales. Incluye funcionalidades para interactuar con una base de datos **SQLite** y conectarse a la **API de Spotify**.

## Características

### Usuarios
- **Crear usuario**: Añade un nuevo usuario.
- **Consultar usuarios**: Obtiene todos los usuarios.
- **Actualizar usuario**: Modifica los datos de un usuario existente.
- **Eliminar usuario**: Elimina un usuario y sus preferencias asociadas.

### Preferencias musicales
- **Artistas favoritos**:
  - Añadir un artista a la lista de favoritos de un usuario.
  - Eliminar un artista de la lista de favoritos de un usuario.
  - Consultar artistas favoritos de un usuario.
- **Canciones favoritas**:
  - Añadir una canción a la lista de favoritos de un usuario.
  - Eliminar una canción de la lista de favoritos de un usuario.
  - Consultar canciones favoritas de un usuario.

### Conexión con Spotify
- **Buscar artista por nombre**: Recupera datos de Spotify sobre un artista específico.
- **Buscar canción por nombre**: Recupera una lista de artistas de Spotify ordenados por popularidad que tengan una canción con el nombre especificado.
- **Buscar canción por nombre y artista**: Recupera datos de Spotify sobre una canción específica.

## Configuración

### Requisitos previos
- Python 3.8+
- Django
- Spotify API Client ID y Client Secret

### Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/DanielCaldes/Django.git
   cd Django
   cd music_api
   ```

2. Crea y activa el entorno virtual (ejemplo con conda):

   ```bash
   conda create --name nombre_del_entorno python=3.x
   conda activate nombre_del_entorno
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tus credenciales de Spotify en un archivo `.env`:
   ```env
   CLIENT_ID="tu_cliente_id"
   CLIENT_SECRET="tu_cliente_secreto"
   ```

### Ejecución

1. Inicia el servidor de FastAPI:
   ```bash
   python manage.py runserver
   ```

2. Accede a la documentación interactiva de la API en Swagger o Redoc:
   http://127.0.0.1:8000/swagger/
   http://127.0.0.1:8000/redoc/

## Endpoints

### Usuarios
#### 1. Crear un usuario

- **Método**: POST
  ```url
  /api/users/
  ```
- **Descripción**: Crea un nuevo usuario y lo agrega a la base de datos.
- **Cuerpo de la solicitud** (JSON):
  ```json
  {
    "username": "nombre"
  }
- **Respuesta**:
  ```json
  {
    "username": "nombre"
  }
  ```


#### 2. Obtener todos los usuarios

- **Método**: GET
  ```url
  /api/users/
  ```
- **Descripción**: Obtiene una lista de todos los usuarios registrados.
- **Respuesta**:
  ```json  
  [
    {
      "username": "nombre"
    },
    {
      "username": "otro_nombre"
    }
  ]
  ```


#### 3. Actualizar un usuario

- **Método**: PUT
  ```url
  /api/users/{user_id}
  ```
- **Descripción**: Actualiza la información de un usuario existente.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "username": "nuevo_nombre"
  }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "nuevo_nombre"
  }
  ```


#### 4. Eliminar un usuario

- **Método**: DELETE
  ```url
  /api/users/{user_id}
  ```
- **Descripción**: Elimina un usuario de la base de datos por su ID.
- **Respuesta**:
  ```json  
  
  ```

### Preferencias musicales
#### 1. Agregar un artista favorito

- **Método**: POST
  ```url
  /api/users/{user_id}/favourites/artists/
  ```
- **Descripción**: Agrega un artista a los favoritos de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "spotify_artist_id": "0TnOYISbd1XYRBk9myaseg"
  }
- **Respuesta**:
  ```json   
  {
    "message": "The artist with id {spotify_artist_id} has been added to the favorites of the user with id {user_id}"
  }
  ```


#### 2. Eliminar un artista favorito

- **Método**: DELETE
  ```url
  /api/users/{user_id}/favourites/artists/
  ```
- **Descripción**: Elimina un artista de los favoritos de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "spotify_artist_id": "0TnOYISbd1XYRBk9myaseg"
  }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "Artist preference removed!"
  }
  ```


#### 3. Obtener artistas favoritos de un usuario

- **Método**: GET
  ```url
  /api/users/{user_id}/favourites/artists/
  ```
- **Descripción**: Obtiene una lista de los artistas favoritos de un usuario por su ID.
- **Respuesta**:
  ```json  
  {
    "favorite_artists": [
      {
        "id": "1EXjXQpDx2pROygh8zvHs4",
        "name": "Melendi",
        "uri": "spotify:artist:1EXjXQpDx2pROygh8zvHs4"
      },
      {
        "id": "5BMgsAFg8rZQc3tqs5BB8G",
        "name": "Mecano",
        "uri": "spotify:artist:5BMgsAFg8rZQc3tqs5BB8G"
      }
    ]
  }
  ```

  
#### 4. Agregar una canción favorita

- **Método**: POST
  ```url
  /api/users/{user_id}/favourites/tracks/
  ```
- **Descripción**: Agrega una canción a los favoritos de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "spotify_track_id": "11dFghVXANMlKmJXsNCbNl"
  }
- Respuesta:
  ```json
  {
    "message": "The track with id {spotify_track_id} has been added to the favourites of the user with id {user_id}."
  }
  ```


#### 5. Eliminar una canción favorita

- **Método**: DELETE
  ```url
  /api/users/{user_id}/favourites/tracks/
  ```
- **Descripción**: Elimina una canción de los favoritos de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "spotify_track_id": "11dFghVXANMlKmJXsNCbNl"
  }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "Track preference removed!"
  }
  ```


#### 6. Obtener canciones favoritas de un usuario

- **Método**: GET
  ```url
  /api/users/{user_id}/favourites/tracks/
  ```
- **Descripción**: Obtiene una lista de las canciones favoritas de un usuario por su ID.
- **Respuesta**:
  ```json  
  {
    "favorite_tracks": [
      {
        "id": "11dFghVXANMlKmJXsNCbNl",
        "name": "Cut To The Feeling",
        "uri": "spotify:track:11dFghVXANMlKmJXsNCbNl",
        "artists": [
          {
            "name": "Carly Rae Jepsen",
            "id": "6sFIWsNpZYqfjUpaCgueju",
            "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
          }
        ]
      }
    ]
  }
  ```


### Conexión con Spotify
#### 1. Buscar un artista en Spotify

- **Método**: GET
  ```url
  /api/spotify/artists/{artist_name}
  ```
- **Descripción**: Busca información de un artista en Spotify.
- **Respuesta**:
  ```json   
  {
    "name": "Pitbull",
    "id": "0TnOYISbd1XYRBk9myaseg",
    "uri": "spotify:artist:0TnOYISbd1XYRBk9myaseg"
  }
  ``` 


#### 2. Buscar una canción en Spotify por nombre

- **Método**: GET
  ```url
  /api/spotify/tracks/{track_name}
  ```
- **Descripción**: Busca los nombres de los artistas posibles para esa canción ordenados por popularidad.
- **Respuesta**:
  ```json  
  [
    {
      "artist_name": "Carly Rae Jepsen",
      "track_popularity": 56
    },
    {
      "artist_name": "Elijah Mann",
      "track_popularity": 27
    },
    {
      "artist_name": "Yawning Portal",
      "track_popularity": 24
    },
    {
      "artist_name": "Kid Froopy",
      "track_popularity": 14
    }
  ]
  ```

#### 3. Buscar una canción en Spotify por nombre y artista

- **Método**: GET
  ```url
  /api/spotify/tracks/{track_name}/{artist_name}
  ```
- **Descripción**: Busca los nombres de los artistas posibles para esa canción ordenados por popularidad.
- **Respuesta**:
  ```json  
  {
    "name": "Cut To The Feeling",
    "id": "6EJiVf7U0p1BBfs0qqeb1f",
    "uri": "spotify:track:6EJiVf7U0p1BBfs0qqeb1f",
    "artists": [
      {
        "name": "Carly Rae Jepsen",
        "id": "6sFIWsNpZYqfjUpaCgueju",
        "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
      }
    ]
  }
  ```
