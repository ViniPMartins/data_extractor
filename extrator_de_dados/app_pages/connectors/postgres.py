import streamlit as st

# Página de configuração de destinos de dados
@st.dialog("Configuração de Conexão - Postgres", width='large')
def configure_postgres_connector():
    #st.header("Configuração do Destino - Postgres")

    # Formulário para configurar dados de conexão do Postgres como destino
    with st.form("postgres_connector_form"):
        name = st.text_input("Nome da Conexão", placeholder="Ex: Postgres")
        host = st.text_input("Host", placeholder="ex: localhost")
        port = st.text_input("Porta", placeholder="ex: 5432")
        database = st.text_input("Banco de Dados", placeholder="ex: my_database")
        user = st.text_input("Usuário", placeholder="ex: postgres")
        password = st.text_input("Senha", type="password")

        # Botão para submeter o formulário
        submit_button = st.form_submit_button("Conectar")

        if submit_button:
            st.success(f"Conexão configurada: banco de dados {database} em {host}:{port} com o usuário {user}!")
            return {
                'name':name,
                'type':'postgres',
                'config':{
                    'host':host,
                    'port':port,
                    'databse':database,
                    'user':user,
                    'password':password
                }
            }