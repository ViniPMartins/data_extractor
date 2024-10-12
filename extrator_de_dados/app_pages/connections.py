import streamlit as st
import time
import pandas as pd
from ..utils.database import MockDatabase
from .connectors.config_connectors import connectors

DATABASE = 'connections'
TABLE = 'connections'

def import_query_connection():
    st.title("Importar query para conexão")
    uploaded_files = st.file_uploader("Selecione uma arquivo .sql para realizar a conexão", type=['sql'])
    return uploaded_files

@st.dialog("Configuração de Conexão", width='large')
def configure_connection(database: MockDatabase, conn_config: dict={}):
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

    sources_list = list(sources.index)
    destination_list = list(destiny.index)

    idx_source = sources_list.index(conn_config['source']) if conn_config else None
    idx_destination = destination_list.index(conn_config['destination']) if conn_config else None

    conn_name = st.text_input("Insira o nome da conexão", value=conn_config.get('name', ''), placeholder="Nome da conexão")
    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox("Selecione a Fonte de Dados", sources_list, index=idx_source, placeholder="Selecionar")
    
    with col2:
        destination = st.selectbox("Selecione o Destino de Dados", destination_list, index=idx_destination, placeholder="Selecionar")

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
        
        data = {
            'config':{
                'name':conn_name,
                "source": source, 
                "destination": destination, 
                "file":uploaded_files
            }
        }

        database.insert_new_data(TABLE, data)

        st.success(f"Conexão estabelecida entre {source} e {destination}!")
        st.session_state.button_connect_disabled = False
        st.session_state.button_close_disabled = True
        
    if st.session_state.button_close_disabled:
        if st.button("Concluir"):
            st.session_state.button_close_disabled = False
            st.rerun()


# Função para exibir as conexões já estabelecidas
def show_connections(database: MockDatabase):
    st.header("Conexões Estabelecidas")

    connections = database.get_table_data(TABLE)

    if len(connections.index) > 0:
        for i, conn in enumerate(connections.index, 1):
            conn_config = connections.loc[conn][0]
            with st.container(height=78, border=True)as tile:
                src = MockDatabase('sources').get_table_data('sources').loc[conn_config['source']]
                dest = MockDatabase('destiny').get_table_data('destiny').loc[conn_config['destination']]

                sub_col1, sub_col2, sub_col3, sub_col4, sub_col5, sub_col6 = st.columns([1,4,1,1,4,2])
                with sub_col1:
                    sub_col1.image(connectors[src['type']]['logo'], width=45)
                with sub_col2:
                    sub_col2.caption('### ' + conn_config['source'])
                with sub_col3:
                    sub_col3.subheader(':material/arrow_right_alt:')
                with sub_col4:
                    sub_col4.image(connectors[dest['type']]['logo'], width=45)
                with sub_col5:
                    sub_col5.caption('### ' + conn_config['destination'])
                with sub_col6:
                    if sub_col6.button(label=":material/edit:", key=str(i) + "-edit", use_container_width=True):
                        configure_connection(database, conn_config)
                # st.write(f"{i}. Fonte: {conn['source']} -> Destino: {conn['destination']}")
    else:
        st.info("Nenhuma conexão estabelecida até o momento.")

# Função principal da página de conexões
def show_connections_page():
    database = MockDatabase(DATABASE)
    
    if 'button_connect_disabled' not in st.session_state:
        st.session_state.button_connect_disabled = False
    if 'button_close_disabled' not in st.session_state:
        st.session_state.button_close_disabled = False

    st.title("Conexões entre Sources e Destinations")
    
    # Seção de configuração de nova conexão
    if st.button("Criar Conexão"):
        configure_connection(database)
    
    st.markdown("---")
    
    # Seção de visualização das conexões estabelecidas
    show_connections(database)

    st.write(database.get_table_data(TABLE))

if __name__ == '__main__':
    show_connections_page()