import streamlit as st
import pandas as pd

class MockDatabase:

    def __init__(self, name: str):
        self.name = name

        if f'config_connectors_{name}' not in st.session_state:
            st.session_state[f'config_connectors_{name}'] = {}

    def get_table_data(self, table: str) -> pd.DataFrame:
        return pd.DataFrame(st.session_state[f'config_connectors_{table}']).T

    def insert_new_data(self, table: str, data: dict):
        st.session_state[f'config_connectors_{table}'][data['config']['name']] = data