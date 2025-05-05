import json
import os
import configparser
from clickhouse_driver import Client
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')

# Configuración de la conexión a ClickHouse
CLICKHOUSE_HOST = config['clickhouse']['host']
CLICKHOUSE_PORT = int(config['clickhouse']['port'])
CLICKHOUSE_DATABASE = config['clickhouse']['database']

# Ruta a la carpeta que contiene los archivos JSON
DATA_FOLDER = 'data'

FIRST_JSON_FILE = 'data/mpd.slice.0-999.json' # Ruta al primer archivo JSON de playlists

# Función para insertar datos en ClickHouse (formato VALUES formateado)
def insert_data(client, table, columns, data):
    """Realiza una inserción de múltiples filas en ClickHouse utilizando la sintaxis INSERT INTO ... VALUES ...

    Args:
        client: Objeto de conexión al cliente de ClickHouse.
        table (str): Nombre de la tabla de destino.
        columns (list): Lista de nombres de las columnas.
        data (list): Una lista de listas o tuplas, donde cada elemento representa una fila de datos a insertar.
                     Los valores en cada fila deben corresponder al orden de las columnas.

    Returns:
        None. Imprime un mensaje de éxito o error en la consola.

    Raises:
        Exception: En caso de error de inserción.
    """
    if data:
        formatted_values = [] # Lista que almacena las filas formateadas para la clausula VALUES
        for row in data:
            formatted_row = [] # Lista que almacena los valores formateados de la fila actual
            for value in row: 

                if isinstance(value, datetime): # Valor es del tipo 'datetime'
                    formatted_row.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")

                elif value is None: # Valor es None
                    formatted_row.append('NULL')

                elif isinstance(value, bool): # Valor es un booleano
                    formatted_row.append(str(int(value))) # Convierto 'True/False' a '1/0' y luego a str

                elif isinstance(value, str): # Valor es un string
                    escaped_value = value.replace("'", "\\'") # Formatea string para SQL, se escapan las comillas 
                    formatted_row.append(f"'{escaped_value}'")

                else: # Valores numericos u otro tipo de dato
                    formatted_row.append(str(value)) # Convierto a str

            # Une los valores formateados de la fila con comas y los encierra entre paréntesis.
            formatted_values.append(f"({','.join(formatted_row)})")
        # Une todas las representaciones de filas con comas para formar la parte VALUES de la consulta.
        values_str = ', '.join(formatted_values)
        # Construye la consulta INSERT completa
        query = f"INSERT INTO {CLICKHOUSE_DATABASE}.{table} ({', '.join(columns)}) VALUES {values_str}"
        #print(f"Query para la tabla: {table} (Valores formateados - primeros 100): {query[:100]}...")
        try:
            client.execute(query) # Ejecuta la consulta SQL en ClickHouse.
            print(f"Se insertaron {len(data)} filas en {table}")
        except Exception as e:
            print(f"Error insertando en {table}: {e}")



if __name__ == '__main__':

    client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, database=CLICKHOUSE_DATABASE)

    # Obtiene la lista de todos los archivos en la carpeta de datos
    all_files = os.listdir(DATA_FOLDER)

    # Filtra la lista para obtener solo los archivos que terminan con '.json'
    json_files = [f for f in all_files if f.endswith('.json')]
    num_json_files = len(json_files) # Obtiene el número de archivos JSON encontrados
    
    print(f"Se encontraron {num_json_files} archivos JSON en la carpeta '{DATA_FOLDER}'.")

    # Pregunta al usuario si desea cargar los archivos, incluyendo el nombre de la base de datos
    confirm = input(f"¿Desea cargar estos {num_json_files} archivos en la base de datos '{CLICKHOUSE_DATABASE}'? (y/n): ").lower()

    if confirm == 'y':
        for json_file in json_files:
            print(f"\n--- Procesando archivo: {json_file} ---")
            playlists_data = [] # Reinicia la lista para cada archivo
            tracks_by_playlist = {} # Reinicia el diccionario para cada archivo
            file_path = os.path.join(DATA_FOLDER, json_file) # Construye la ruta completa al archivo

            try:
                # Cada JSON contiene un diccionario con una clave 'playlists' 
                # cuyo valor es una lista de diccionarios (cada uno representa una playlist).
                with open(FIRST_JSON_FILE, 'r') as f:
                    data = json.load(f)# Carga el contenido del archivo JSON en la variable 'data' como un diccionario.
                    
                    # Itera sobre cada diccionario que representa una playlist dentro de la lista 'playlists' del diccionario 'data'.
                    for playlist_data in data['playlists']:
                        playlist = { # Crea un diccionario para almacenar los datos de cada playlist.
                            'pid': int(playlist_data['pid']),
                            'name': playlist_data.get('name'),
                            'description': playlist_data.get('description'),
                            'modified_at': datetime.fromtimestamp(playlist_data['modified_at']),
                            'num_artists': int(playlist_data['num_artists']),
                            'num_albums': int(playlist_data['num_albums']),
                            'num_tracks': int(playlist_data['num_tracks']),
                            'num_followers': int(playlist_data['num_followers']),
                            'num_edits': int(playlist_data['num_edits']),
                            'duration_ms_total': int(playlist_data['duration_ms']),
                            'collaborative': playlist_data['collaborative'].lower() == 'true'
                        }
                        # Añade los valores del diccionario 'playlist' como una tupla a la lista 'playlists_data'.
                        playlists_data.append(tuple(playlist.values()))

                        playlist_id = int(playlist_data['pid']) # Obtiene el ID de la playlist actual para procesar sus canciones.
                        # Itera sobre cada diccionario que representa una canción ('track') dentro de la lista 'tracks' de la playlist actual.
                        for i, track in enumerate(playlist_data['tracks']):
                            track_info = { # Crea un diccionario para almacenar los datos relevantes de cada canción.
                                'playlist_id': playlist_id,
                                'pos': i,
                                'artist_name': track['artist_name'],
                                'track_uri': track['track_uri'],
                                'artist_uri': track['artist_uri'],
                                'track_name': track['track_name'],
                                'album_uri': track['album_uri'],
                                'duration_ms': int(track['duration_ms']),
                                'album_name': track['album_name']
                            }
                            # Verifica si ya existe una lista de canciones para esta playlist ID en el diccionario.
                            if playlist_id not in tracks_by_playlist: 
                                # Si no existe, crea una lista vacia para las canciones de esta playlist 
                                tracks_by_playlist[playlist_id] = []
                            # Añade los valores del diccionario como una tupla a la lista de canciones correspondiente a su playlist ID.
                            tracks_by_playlist[playlist_id].append(tuple(track_info.values()))
                            
            except FileNotFoundError: 
                print(f"Error: No se encontró el archivo JSON en la ruta: {FIRST_JSON_FILE}")
                exit(1) 
            except json.JSONDecodeError:
                print(f"Error: No se pudo decodificar el JSON del archivo: {FIRST_JSON_FILE}. Asegúrese de que el formato sea válido.")
                exit(1) 

            # Insertar los datos de playlists en la tabla 'playlists' de ClickHouse
            playlists_columns = ['pid', 'name', 'description', 'modified_at', 'num_artists', 'num_albums', 'num_tracks', 'num_followers', 'num_edits', 'duration_ms_total', 'collaborative']
            insert_data(client, 'playlists', playlists_columns, playlists_data)
            print("Se terminó de insertar la información de las playlist. Ahora se insertarán las canciones(tracks).")
            
            # Insertar los datos de tracks en la tabla 'tracks' de ClickHouse, agrupados por 'playlist_id'
            tracks_columns = ['playlist_id', 'pos', 'artist_name', 'track_uri', 'artist_uri', 'track_name', 'album_uri', 'duration_ms', 'album_name']
            for playlist_id, tracks_data_list in tracks_by_playlist.items():
                if tracks_data_list:
                    insert_data(client, 'tracks', tracks_columns, tracks_data_list)

                
        client.disconnect()
        print(f"Se terminaron de cargar los {num_json_files} archivos JSON en la base de datos '{CLICKHOUSE_DATABASE}'.")
    
    else:
        print("Operación de carga cancelada por el usuario.")
        client.disconnect()