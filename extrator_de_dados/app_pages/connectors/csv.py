import streamlit as st

# Página de configuração de destinos de dados
@st.dialog("Configuração de Conexão - CSV")
def configure_csv_connector():
    #st.header("Configuração do Destino - Postgres")

    # Formulário para configurar dados de conexão do Postgres como destino
    with st.form("csv_connector_form"):
        path = st.text_input("File Path", placeholder="ex: C://usuario/meu_arquivo.csv")
        
        # Botão para submeter o formulário
        submit_button = st.form_submit_button("Conectar")

        if submit_button:
            st.success(f"Conexão configurada: Conexão com arquivo {path} configurada")