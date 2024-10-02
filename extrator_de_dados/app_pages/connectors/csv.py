import streamlit as st

# Página de configuração de destinos de dados
@st.dialog("Configuração de Conexão - CSV", width='large')
def configure_csv_connector(db_conn, table, params: dict = {}):

    name = st.text_input("Nome da Conexão", value=params.get('name', ''), placeholder="Ex: Arquivo CSV")
    path = st.text_input("File Path", value=params.get('path', ''), placeholder="ex: C://usuario/meu_arquivo.csv")
    
    if st.button("Conectar"):
        st.success(f"Conexão configurada: Conexão com arquivo {path} configurada")
        data = {
            'type':'csv',
            'config':{
                'name':name,
                'path':path
            }
        }
        db_conn.insert_new_data(table, data)
        st.rerun()