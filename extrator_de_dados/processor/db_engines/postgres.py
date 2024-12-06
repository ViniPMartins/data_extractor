from .abstract_engine import AbstractEngine
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd


class PostgresEngine(AbstractEngine):
    """
    Implementação de um motor de banco de dados para PostgreSQL.
    """
    def __init__(self, config):
        self._validate_config(config)
        self.url_engine = self._create_connection_url(config)

    def _validate_config(self, config):
        required_keys = {'user', 'password', 'host', 'port', 'database'}
        missing_keys = required_keys - config.keys()
        if missing_keys:
            raise ValueError("Configuração incompleta. É necessario ter as seguintes chaves preenchidas: {'user', 'password', 'host', 'port', 'database'}")

    def _create_connection_url(self, config):
        """
        Gera a URL de conexão para o banco de dados PostgreSQL.
        """
        return (
            f"postgresql+psycopg2://{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{config['database']}"
        )

    def connect(self):
        """
        Cria e retorna uma conexão com o banco de dados.
        """
        try:
            engine = create_engine(self.url_engine)
            return engine.connect()
        except SQLAlchemyError as e:
            raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

    def execute_query(self, query):
        """
        Executa uma consulta no banco de dados e retorna os resultados como um DataFrame.
        """
        try:
            with self.connect() as conn:
                return pd.read_sql_query(text(query), conn)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro ao executar consulta: {e}")

    def insert_data(self, table, data):
        """
        Insere dados em uma tabela do banco de dados.
        """
        try:
            with self.connect() as conn:
                data.to_sql(table, con=conn, if_exists='append', index=False)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro ao inserir dados: {e}")
