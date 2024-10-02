import streamlit as st
import time
import pandas as pd
from ..utils.database import MockDatabase

# Simulando fontes e destinos configurados
connections = []

def import_query_connection():
    st.title("Importar query para conexão")
    uploaded_files = st.file_uploader("Selecione uma arquivo .sql para realizar a conexão", type=['sql'])
    return uploaded_files

    # if uploaded_files:
    #     bytes_data = uploaded_files.read()
    #     st.write("filename:", uploaded_files.name)
    #     st.write(bytes_data)

@st.dialog("Configuração de Conexão", width='large')
def configure_connection():
    def disable_button():
        st.session_state.button_connect_disabled = True

    def check_values():
        if not source: 
            st.error("Escolha um fonte de dados")
            return False
        elif not destination:
            st.error("Escolha um destino para os dados")
            return False
        elif not uploaded_files:
            st.error("Escolha um arquivo")
            return False
        else:
            st.success("Todas as informações preenchidas")
            return True


    sources = MockDatabase('sources').get_table_data('sources')
    destiny = MockDatabase('destiny').get_table_data('destiny')

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox("Selecione a Fonte de Dados", [s for s in sources.index], index=None, placeholder="Selecionar")
    
    with col2:
        destination = st.selectbox("Selecione o Destino de Dados", [d for d in destiny.index], index=None, placeholder="Selecionar")

    st.title("Importar query para conexão")
    uploaded_files = st.file_uploader("Selecione uma arquivo .sql para realizar a conexão", type=['sql'])
    
    if not st.session_state.button_connect_disabled:
        if check_values() and st.button("Conectar", on_click=disable_button, disabled=st.session_state.button_connect_disabled):
            st.session_state.button_connect_disabled = True
    else:
        with st.status("Validando Conexão", expanded=True):
            st.write("Conectando com a origem...")
            time.sleep(2)
            st.write("Conectando com o Destino...")
            time.sleep(1)
            st.write("Validando Query SQL")
            time.sleep(1)
        
        connections.append({"source": source, "destination": destination})
        st.success(f"Conexão estabelecida entre {source} e {destination}!")
        st.session_state.button_connect_disabled = False
        st.session_state.button_close_disabled = True
        
    if st.session_state.button_close_disabled:
        if st.button("Concluir"):
            st.session_state.button_close_disabled = False
            st.rerun()


# Função para exibir as conexões já estabelecidas
def show_connections():
    st.header("Conexões Estabelecidas")

    if connections:
        for i, conn in enumerate(connections, 1):
            st.write(f"{i}. Fonte: {conn['source']} -> Destino: {conn['destination']}")
    else:
        st.info("Nenhuma conexão estabelecida até o momento.")

# Função principal da página de conexões
def show_connections_page():
    
    if 'button_connect_disabled' not in st.session_state:
        st.session_state.button_connect_disabled = False
    if 'button_close_disabled' not in st.session_state:
        st.session_state.button_close_disabled = False

    st.title("Conexões entre Sources e Destinations")
    
    # Seção de configuração de nova conexão
    if st.button("Criar Conexão"):
        configure_connection()
    
    st.markdown("---")
    
    # Seção de visualização das conexões estabelecidas
    show_connections()

if __name__ == '__main__':
    show_connections_page()