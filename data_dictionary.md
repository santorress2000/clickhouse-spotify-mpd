## Diccionario de Datos

Este diccionario de datos describe la estructura y el contenido de las tablas `playlists` y `tracks` en la base de datos `spotify_mpd` de ClickHouse.

**Tabla: `playlists`**

| Nombre de la Columna | Tipo de Dato | Descripción | Ejemplo de Valor |
| ---------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `pid` | `UInt32` | Identificador único de la playlist. | 12345 |
| `name` | `String` | Nombre de la playlist. | "My Favorites" |
| `description` | `Nullable(String)` | Descripción de la playlist (puede ser nula). | "Chill vibes..." |
| `modified_at` | `DateTime` | Timestamp de la última modificación de la playlist. | "2024-07-28 10:00:00" |
| `num_artists` | `UInt16` | Número de artistas únicos en la playlist. | 25 |
| `num_albums` | `UInt16` | Número de álbumes únicos en la playlist. | 15 |
| `num_tracks` | `UInt16` | Número total de canciones en la playlist. | 100 |
| `num_followers` | `UInt32` | Número de seguidores de la playlist. | 500 |
| `num_edits` | `UInt16` | Número de sesiones de edición de la playlist. | 10 |
| `duration_ms_total` | `UInt32` | Duración total de todas las canciones en la playlist (en milisegundos). | 3600000 |
| `collaborative` | `Bool` | Indica si la playlist es colaborativa (1: Verdadero, 0: Falso). | 1 |

**Tabla: `tracks`**

| Nombre de la Columna | Tipo de Dato | Descripción | Ejemplo de Valor |
| ------------------- | ---------- | ----------------------------------------------------------------------------------------------------------- | ---------------- |
| `playlist_id` | `UInt32` | Identificador de la playlist a la que pertenece la canción (clave foránea de `playlists.pid`). | 12345 |
| `pos` | `UInt16` | Posición de la canción dentro de la playlist. | 1 |
| `artist_name` | `String` | Nombre del artista de la canción. | "The Beatles" |
| `track_uri` | `String` | URI de la canción en Spotify. | "spotify:track:..." |
| `artist_uri` | `String` | URI del artista en Spotify. | "spotify:artist:..." |
| `track_name` | `String` | Nombre de la canción. | "Hey Jude" |
| `album_uri` | `String` | URI del álbum en Spotify. | "spotify:album:..." |
| `duration_ms` | `UInt32` | Duración de la canción en milisegundos. | 240000 |
| `album_name` | `String` | Nombre del álbum de la canción. | "Abbey Road" |