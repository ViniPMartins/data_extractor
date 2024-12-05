import streamlit as st
from ...utils.validators import check_fill_connectors_values
import uuid

# Página de configuração de destinos de dados
@st.dialog("Configuração de Conexão - CSV", width='large')
def configure_csv_connector(db_conn, table, params: dict = {'config':'{}'}, id: str = None):

    configs: dict = eval(params['config'])

    conn_id = id if id else str(uuid.uuid4())
    name = st.text_input("Nome da Conexão", value=params.get('name', ''), placeholder="Ex: Arquivo CSV")
    path = st.text_input("File Path", value=configs.get('path', ''), placeholder="ex: C://usuario/meu_arquivo.csv")
    
    config = {
        'path':path
    }

    data = [{
        'type':'csv',
        'name':name,
        'uuid':conn_id,
        'config':str(config)
    }]
    
    if check_fill_connectors_values(config) and st.button("Conectar"):
        st.success(f"Conexão configurada: Conexão com arquivo {path} configurada")

        if id:
            db_conn.update_data(table, data)
        else:
            db_conn.insert_new_data(table, data)
        st.rerun()