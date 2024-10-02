import streamlit as st

def check_values(data: dict):
    for k, v in data.items():
        if not v:
            st.error(f"Insira um valor para o parâmetro {k}")
            return False
    return True

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
    
    if check_values(data['config']) and st.button("Conectar"):
        st.success(f"Conexão configurada: Conexão com arquivo {path} configurada")

        db_conn.insert_new_data(table, data)
        st.rerun()