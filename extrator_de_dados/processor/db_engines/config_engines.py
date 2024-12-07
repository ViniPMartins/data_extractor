from .postgres import PostgresEngine
from .mysql import MysqlEngine
from .csv import CsvEngine

engines = {
    'postgres': PostgresEngine,
    'mysql': MysqlEngine,
    'csv':CsvEngine
}