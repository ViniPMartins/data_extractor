import streamlit as st

# Página de configuração de destinos de dados
@st.dialog("Configuração de Conexão - MySQL", width='large')
def configure_mysql_connector(db_conn, table, params: dict = {}):

    name = st.text_input("Nome da Conexão", value=params.get('name', ''), placeholder="Ex: database name")
    host = st.text_input("Host", value=params.get('host', ''), placeholder="ex: localhost")
    port = st.text_input("Porta", value=params.get('port', ''), placeholder="ex: 5432")
    database = st.text_input("Banco de Dados", value=params.get('database', ''), placeholder="ex: my_database")
    user = st.text_input("Usuário", value=params.get('user', ''), placeholder="ex: user")
    password = st.text_input("Senha", value=params.get('password', ''), type="password")

    if st.button("Conectar"):
        st.success(f"Conexão configurada: banco de dados {database} em {host}:{port} com o usuário {user}!")
        data = {
            'type':'mysql',
            'config':{
                'name':name,
                'host':host,
                'port':port,
                'database':database,
                'user':user,
                'password':password
            }
        }
        db_conn.insert_new_data(table, data)
        st.rerun()