import os

# Importação das configurações de cada conector
from .postgres import configure_postgres_connector
from .mysql import configure_mysql_connector
from .csv import configure_csv_connector

def get_image_path(image_name):
    return os.path.join(os.path.dirname(__file__), '../../assets', image_name)

connectors = {
    'postgres': {"name":"Banco Postgres", "logo":get_image_path("postgres_logo.png"), "config":configure_postgres_connector},
    'mysql': {"name":"Banco Mysql", "logo":get_image_path("mysql_logo.png"), "config":configure_mysql_connector},
    'csv': {"name":"Arquivo CSV", "logo":get_image_path("csv_logo.png"), "config":configure_csv_connector},
}