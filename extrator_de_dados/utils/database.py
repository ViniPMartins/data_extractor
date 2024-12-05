import streamlit as st
import sqlalchemy as sa
from sqlalchemy import create_engine
import pandas as pd
import duckdb
from typing import Optional

class MockDatabase:

    def __init__(self, name: str):
        self.name = name

        if f'config_connectors_{name}' not in st.session_state:
            st.session_state[f'config_connectors_{name}'] = {}

    def get_table_data(self, table: str) -> pd.DataFrame:
        return pd.DataFrame(st.session_state[f'config_connectors_{table}']).T

    def insert_new_data(self, table: str, data: dict):
        st.session_state[f'config_connectors_{table}'][data['uuid']] = data

    def delete_data(self, table: str, data_id: str | int):
        st.session_state[f'config_connectors_{table}'].pop(data_id)

class InternalDataBase:
    def __init__(self, database):
        self.database = database
        self.connection = None
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine(f'sqlite:///{self.database}.db')
            return self.engine.connect()
        except Exception as e:
            print(f"Não foi possível conectar: {e}")
            return None
    
    def get_table_data(self, table: str = None) -> pd.DataFrame:
        try:
            with self.connect() as con:
                df_table = pd.read_sql_table(table, con, index_col='uuid')
            return df_table
        except Exception as e:
            print(f"Erro ao carregar dados da tabela {table}")
            print(e)
            return None
            
    def insert_new_data(self, table: str, data: dict) -> None:

        new_data = pd.DataFrame(data).set_index('uuid')

        table_data: Optional[pd.DataFrame] = self.get_table_data(table)
        if table_data is None:
            df = new_data
        else:    
            df = pd.concat([table_data, new_data])

        with self.connect() as con:
            if not con:
                print("Você não está conectado")
            else:
                df.to_sql(table, con, if_exists='replace')

    def update_data(self, table: str, data: dict) -> None:

        id = data[0]['uuid']
        table_data: Optional[pd.DataFrame] = self.get_table_data(table)
        table_data_clean = table_data.drop(id)
        new_data = pd.DataFrame(data).set_index('uuid')
        df = pd.concat([table_data_clean, new_data])

        with self.connect() as con:
            if not con:
                print("Você não está conectado")
            else:
                df.to_sql(table, con, if_exists='replace')


    def delete_data(self, table: str, data_id: str | int) -> None:

        table_data: Optional[pd.DataFrame] = self.get_table_data(table)
        df = table_data.drop(data_id)

        with self.connect() as con:
            if not con:
                print("Você não está conectado")
            else:
                df.to_sql(table, con, if_exists='replace')
