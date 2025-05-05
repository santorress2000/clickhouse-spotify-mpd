-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS spotify_mpd;

-- Usar la base de datos spotify_mpd
USE spotify_mpd;

--
-- Tabla: playlists
-- Contiene información general sobre cada playlist única.
--
CREATE TABLE IF NOT EXISTS playlists (
    pid UInt32,             -- Identificador único de la playlist (Playlist ID)
    name String,             -- Nombre de la playlist
    description Nullable(String), -- Descripción de la playlist (puede ser nula)
    modified_at DateTime,     -- Timestamp de la última modificación de la playlist
    num_artists UInt16,      -- Número de artistas únicos en la playlist
    num_albums UInt16,       -- Número de álbumes únicos en la playlist
    num_tracks UInt16,       -- Número total de canciones en la playlist
    num_followers UInt32,    -- Número de seguidores de la playlist
    num_edits UInt16,        -- Número de sesiones de edición de la playlist
    duration_ms_total UInt32, -- Duración total de todas las canciones en la playlist (en milisegundos)
    collaborative Bool       -- Indica si la playlist es colaborativa (true/false)
) ENGINE = MergeTree()
ORDER BY pid;

--
-- Tabla: tracks
-- Contiene información sobre cada canción individual dentro de las playlists.
-- Cada fila representa una canción en una playlist específica.
--
CREATE TABLE IF NOT EXISTS tracks (
    playlist_id UInt32,    -- Identificador de la playlist a la que pertenece la canción (clave foránea implícita a playlists.pid)
    pos UInt16,            -- Posición de la canción dentro de la playlist
    artist_name String,     -- Nombre del artista de la canción
    track_uri String,        -- URI de la canción en Spotify
    artist_uri String,       -- URI del artista en Spotify
    track_name String,       -- Nombre de la canción
    album_uri String,        -- URI del álbum en Spotify
    duration_ms UInt32,     -- Duración de la canción (en milisegundos)
    album_name String       -- Nombre del álbum de la canción
) ENGINE = MergeTree()
PARTITION BY playlist_id
ORDER BY (playlist_id, pos);

