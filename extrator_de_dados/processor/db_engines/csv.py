from .abstract_engine import AbstractEngine
import pandas as pd

class CsvEngine(AbstractEngine):

    def __init__(self, config):
        self._validate_config(config)
        self.csv_path = self._create_connection_url(config)

    def _validate_config(self, config):
        required_keys = {'path'}
        missing_keys = required_keys - config.keys()
        if missing_keys:
            raise ValueError("Configuração incompleta. É necessario ter as seguintes chaves preenchidas: {'path'}")

    def _create_connection_url(self, config):
        return (config['path'])

    def connect(self):
        pass
    
    def execute_query(self, *args, **kargs):
        return pd.read_csv(self.csv_path, encoding='utf-8')
    
    def insert_data(self, table, data: pd.DataFrame):
        data.to_csv(self.csv_path)