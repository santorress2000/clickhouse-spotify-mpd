-- Contar el número total de playlists
SELECT COUNT() FROM playlists;

-- Contar el número total de canciones en la tabla tracks
SELECT COUNT() FROM tracks;

-- Contar el número total de canciones en la tabla tracks
SELECT COUNT() FROM tracks;

-- Calcular la duración promedio de las canciones (en ms)
SELECT AVG(duration_ms) FROM tracks;

-- Calcular el número promedio de canciones por playlist
SELECT AVG(num_tracks) FROM playlists;

-- Encontrar la playlist con el menor número de canciones
SELECT MIN(num_tracks) FROM playlists;

-- Encontrar la canción más larga (en ms)
SELECT MAX(duration_ms) FROM tracks;

-- Los 10 artistas mas repetidos en tracks
SELECT artist_name, COUNT(*) AS count
FROM spotify_mpd.tracks
GROUP BY artist_name
ORDER BY count DESC
LIMIT 10;

-- Encontrar las 5 playlists con más seguidores
SELECT name, num_followers
FROM playlists
ORDER BY num_followers DESC
LIMIT 5;

-- Encontrar las 10 canciones más largas
SELECT track_name, artist_name, duration_ms
FROM tracks
ORDER BY duration_ms DESC
LIMIT 10;