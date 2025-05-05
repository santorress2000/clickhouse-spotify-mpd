## Implementación de Base de Datos Columnar con ClickHouse
### Asignatura: Técnicas y Herramientas para Datos Masivos

## Descripción del Proyecto

Este proyecto implementa una base de datos NoSQL orientada a columnas utilizando ClickHouse para analizar un subconjunto del "Spotify Million Playlist Dataset Challenge" (disponible en [https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)).Debido al gran tamaño del dataset original (1 millón de playlists), para esta actividad se utilizó un subconjunto de aproximadamente 80,000 playlists, que comprenden alrededor de 5.4 millones de canciones (tracks). 

Los datos originales, distribuidos en múltiples archivos JSON (cada uno conteniendo 1000 playlists), fueron procesados mediante un proceso de **Extracción, Transformación y Carga (ETL)** implementado en el script `ETL.py`. Este script lee los archivos JSON, transforma los datos necesarios y finalmente los carga en la base de datos columnar ClickHouse para su almacenamiento eficiente y posterior análisis. 

Para la exploración inicial de los datos almacenados, se utilizó Metabase para la creación de visualizaciones gráficas.

### Estructura del Proyecto:
```
├── config.ini        # Configuración de la conexión a ClickHouse
├── data/             # Archivos JSON del dataset
│   └── ...
├── DDL.sql           # Esquema de la base de datos ClickHouse
├── ETL.py            # Script para cargar datos a ClickHouse
└── queries.sql       # Consultas SQL de ejemplo
└── README.md
```

### Prerrequisitos:

* **ClickHouse:** Debe estar instalado y en ejecución.
    **Instalación de ClickHouse:**

    Para una guía rápida y detallada sobre cómo instalar ClickHouse en diferentes sistemas operativos, consulta la página oficial de inicio rápido: [https://clickhouse.com/docs/getting-started/quick-start](https://clickhouse.com/docs/getting-started/quick-start)

* **Python:** Versión **3.6 o superior**.
* **Librerías de Python:**
    ```bash
    pip install clickhouse-driver
    ```

### Descarga de los datos

Los datos utilizados del "Spotify Million Playlist Dataset" se encuentran disponibles en la siguiente carpeta de Google Drive: https://drive.google.com/drive/folders/1kBeGaAEfBICQImlhC_PHEgHdkZ7yX9yo?usp=sharing.

Debes descargar el contenido de esta carpeta y colocarlo en el directorio `data/` de tu proyecto.

### **Creación de la Base de Datos `spotify_mpd`:**

Una vez que ClickHouse esté en ejecución, puedes crear la base de datos utilizando el cliente de ClickHouse:

1.  Abre la línea de comandos en la carpeta donde instalaste ClickHouse y ejecuta:
    ```bash
    clickhouse-client
    ```
2.  Dentro del cliente de ClickHouse, ejecuta la siguiente consulta:
    ```sql
    CREATE DATABASE IF NOT EXISTS spotify_mpd;
    ```
3.  Para usar la base de datos, ejecuta:
    ```sql
    USE spotify_mpd;
    ``` 
4.  A continuación, crea las tablas `playlists` y `tracks` ejecutando las sentencias DDL que se encuentran en el archivo DDL.sql.
    Para hacerlo, copia las sentencias del archivo y ejecutalas en el cliente de ClickHouse. 

