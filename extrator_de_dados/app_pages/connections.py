import streamlit as st
import time
import pandas as pd
from ..utils.database import MockDatabase
from .connectors.config_connectors import connectors
from io import StringIO
from code_editor import code_editor
import json
import uuid

with open('extrator_de_dados/app_pages/code_editor_btns.json') as json_button_file:
    custom_buttons = json.load(json_button_file)

DATABASE = 'connections'
TABLE = 'connections'

@st.dialog("Excluir Conexão")
def delete_connection(database: MockDatabase, df: pd.DataFrame, r: int):
    conn_name = df.loc[r]['name']
    st.write(f'Digite `{conn_name}` abaixo para deletar a conexão')
    input_name = st.text_input('', label_visibility='hidden')

    if st.button("Deletar"): 
        if conn_name == input_name:
            uuid = df.loc[r]['uuid']
            database.delete_data(TABLE, uuid)
            st.rerun()
        else:
            st.error('O nome da conexão está incorreto')


def import_query_connection():
    st.title("Importar query para conexão")
    uploaded_files = st.file_uploader("Selecione uma arquivo .sql para realizar a conexão", type=['sql'])
    return uploaded_files

@st.dialog("Configuração de Conexão", width='large')
def configure_connection(database: MockDatabase, conn_params: dict={}):

    def disable_button():
        st.session_state.button_connect_disabled = True

    def check_values(conn_name=None, source=None, destination=None, query=None):
        if not conn_name:
            st.error("Escolha um nome da fonte de dados")
            return False
        elif not source: 
            st.error("Escolha um fonte de dados")
            return False
        elif not destination:
            st.error("Escolha um destino para os dados")
            return False
        elif not query:
            st.error("Salve um query para realizar a extração")
            return False
        else:
            st.success("Todas as informações preenchidas")
            return True
        
    conn_id = conn_params['uuid'] if conn_params.get('uuid', None) else str(uuid.uuid4())

    sources = MockDatabase('sources').get_table_data('sources')
    destiny = MockDatabase('destiny').get_table_data('destiny')

    def name_source_connection(options):
        return sources.loc[options]['name']
    
    def name_destination_connection(options):
        return destiny.loc[options]['name']
    
    sources_list = list(sources.index) if len(sources) > 0 else {}
    destination_list = list(destiny.index) if len(destiny) > 0 else {}

    idx_source = sources_list.index(conn_params['config']['source']) if conn_params.get('config', None) else None
    idx_destination = destination_list.index(conn_params['config']['destination']) if conn_params.get('config', None) else None

    conn_name = st.text_input("Insira o nome da conexão", value=conn_params.get('name', ''), placeholder="Nome da conexão")
    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox("Selecione a Fonte de Dados", sources_list, format_func=name_source_connection, index=idx_source, placeholder="Selecionar", )
    with col2:
        destination = st.selectbox("Selecione o Destino de Dados", destination_list, format_func=name_destination_connection, index=idx_destination, placeholder="Selecionar")

    st.title("Importar query para conexão")
    if conn_params.get('config', None):
        editor = code_editor(conn_params['config']['file'], lang='sql', buttons=custom_buttons, allow_reset=True)
        st.write(editor)

        if editor['type'] == "submit" and len(editor['text']) != 0:
            query = editor['text']
            editor['type'] = ""
            st.success("Alteração salva com sucesso")
        else:
            query = None
    else:
        uploaded_files = st.file_uploader("Selecione uma arquivo .sql para realizar a conexão", type=['sql'])
        if uploaded_files:
            stringio = StringIO(uploaded_files.getvalue().decode("utf-8"))
            query = stringio.read()
        else:
            query = None
    
    if not st.session_state.button_connect_disabled:
        if check_values(conn_name, source, destination, query) and st.button("Conectar", on_click=disable_button, disabled=st.session_state.button_connect_disabled):
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
            'uuid':conn_id,
            'name':conn_name,
            'config':{
                "source": source, 
                "destination": destination, 
                "file":query
            }
        }

        database.insert_new_data(TABLE, data)

        st.success(f"{conn_name} criada com sucesso!")
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
        for i, conn in enumerate(connections.index, 0):
            conn_config = connections.loc[conn]['config']
            with st.container(height=78, border=True) as tile:
                src = MockDatabase('sources').get_table_data('sources').loc[conn_config['source']]
                dest = MockDatabase('destiny').get_table_data('destiny').loc[conn_config['destination']]

                name_conn, logo_1, name_1, arrow, logo_2, name_2, edit_btn, delete_btn = st.columns([6,1,4,2,1,4,2,2])

                with name_conn:
                    st.caption('### ' + connections.loc[conn]['name'])
                with logo_1:
                    st.image(connectors[src['type']]['logo'], width=45)
                with name_1:
                    st.caption('### ' + src['name'])
                with arrow:
                    st.subheader(':material/arrow_right_alt:')
                with logo_2:
                    st.image(connectors[dest['type']]['logo'], width=45)
                with name_2:
                    st.caption('### ' + dest['name'])
                with edit_btn:
                    if st.button(label=":material/edit:", key=str(i) + "-edit", use_container_width=True):
                        configure_connection(database, connections.loc[conn])
                with delete_btn:
                    if st.button(label=":material/delete:", key=str(i) + "-delete", use_container_width=True):
                        uuid = connections.loc[conn]['uuid']
                        delete_connection(database, connections, uuid)

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

    #st.write(database.get_table_data(TABLE))

if __name__ == '__main__':
    show_connections_page()