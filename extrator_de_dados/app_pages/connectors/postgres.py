import streamlit as st
from ...utils.validators import check_fill_connectors_values
import uuid

# Página de configuração de destinos de dados
@st.dialog("Configuração de Conexão - Postgres", width='large')
def configure_postgres_connector(db_conn, table, params: dict = {'config':'{}'}, id: str = None):

    configs: dict = eval(params['config'])

    conn_id = id if id else str(uuid.uuid4())
    name = st.text_input("Nome da Conexão", value=params.get('name', ''), placeholder="Ex: database name")
    host = st.text_input("Host", value=configs.get('host', ''), placeholder="ex: localhost")
    port = st.text_input("Porta", value=configs.get('port', ''), placeholder="ex: 5432")
    database = st.text_input("Banco de Dados", value=configs.get('database', ''), placeholder="ex: my_database")
    user = st.text_input("Usuário", value=configs.get('user', ''), placeholder="ex: user")
    password = st.text_input("Senha", value=configs.get('password', ''), type="password")

    config = {
            'host':host,
            'port':port,
            'database':database,
            'user':user,
            'password':password
        }
    
    data = [{
        'type':'postgres',
        'name':name,
        'uuid':conn_id,
        'config':str(config)
    }]

    if check_fill_connectors_values(config) and st.button("Conectar"):
        st.success(f"Conexão configurada: banco de dados {database} em {host}:{port} com o usuário {user}!")
        if id:
            db_conn.update_data(table, data)
        else:
            db_conn.insert_new_data(table, data)
        #st.session_state.config_connectors[name] = conn
        st.rerun()