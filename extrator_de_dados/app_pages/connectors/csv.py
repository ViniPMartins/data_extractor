import streamlit as st
from ...utils.validators import check_fill_connectors_values

# Página de configuração de destinos de dados
@st.dialog("Configuração de Conexão - CSV", width='large')
def configure_csv_connector(db_conn, table, params: dict = {}):

    name = st.text_input("Nome da Conexão", value=params.get('name', ''), placeholder="Ex: Arquivo CSV")
    path = st.text_input("File Path", value=params.get('path', ''), placeholder="ex: C://usuario/meu_arquivo.csv")
    data = {
        'type':'csv',
        'config':{
            'name':name,
            'path':path
        }
    }
    
    if check_fill_connectors_values(data['config']) and st.button("Conectar"):
        st.success(f"Conexão configurada: Conexão com arquivo {path} configurada")

        db_conn.insert_new_data(table, data)
        st.rerun()