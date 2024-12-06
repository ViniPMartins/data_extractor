from .abstract_engine import AbstractEngine
from sqlalchemy import create_engine, text
import pandas as pd

class PostgresEngine(AbstractEngine):

    def __init__(self, config):
        self.url_engine = self.engine(config)

    def engine(self, config):
        url = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        return url
    
    def connect(self):
        try:
            self.engine = create_engine(self.url_engine)
            return self.engine.connect()
        except Exception as e:
            print(f"Não foi possível conectar: {e}")

    def execute_query(self, query):
        """Executa a query em um banco de dados de origem e retorna os resultados como um DataFrame."""
        with self.connect() as conn:
            result = pd.read_sql_query(text(query), conn)
        return result
    
    def insert_data(self, table, data):
         with self.connect() as conn:
            data.to_sql(table, con=conn, if_exists='append', index=False)