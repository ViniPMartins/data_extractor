import streamlit as st

def check_fill_connectors_values(data: dict):
    for k, v in data.items():
        if not v:
            st.error(f"Insira um valor para o parâmetro {k}")
            return False
    return True
