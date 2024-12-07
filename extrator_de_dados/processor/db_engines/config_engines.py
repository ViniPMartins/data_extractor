from .postgres import PostgresEngine
from .mysql import MysqlEngine

engines = {
    'postgres': PostgresEngine,
    'mysql': MysqlEngine
}