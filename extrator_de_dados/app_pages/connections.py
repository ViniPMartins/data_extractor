import streamlit as st
import time
import pandas as pd
from ..utils.database import InternalDataBase
from .connectors.config_connectors import connectors
from io import StringIO
from code_editor import code_editor
import json
import uuid
from typing import Optional
from ..processor.extrator_processor import run_processor

with open('extrator_de_dados/app_pages/code_editor_btns.json') as json_button_file:
    custom_buttons = json.load(json_button_file)

DATABASE = 'internal'
TABLE = 'connections'

@st.dialog("Excluir Conexão")
def delete_connection(database: InternalDataBase, df: pd.DataFrame, id: int):
    conn_name = df.loc[id]['name']
    st.write(f'Digite `{conn_name}` abaixo para deletar a conexão')
    input_name = st.text_input('', label_visibility='hidden')

    if st.button("Deletar"): 
        if conn_name == input_name: 
            database.delete_data(TABLE, id)
            st.rerun()
        else:
            st.error('O nome da conexão está incorreto')


def import_query_connection():
    st.title("Importar query para conexão")
    uploaded_files = st.file_uploader("Selecione uma arquivo .sql para realizar a conexão", type=['sql'])
    return uploaded_files

@st.dialog("Configuração de Conexão", width='large')
def configure_connection(database: InternalDataBase, conn_params: Optional[dict] = {} ):

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
        elif not table_name:
            st.error("Escolha um destino para os dados")
            return False
        elif not query:
            st.error("Salve um query para realizar a extração")
            return False
        else:
            st.success("Todas as informações preenchidas")
            return True
    
    conn_id = conn_params.name if isinstance(conn_params, pd.Series) else str(uuid.uuid4())

    sources = InternalDataBase(DATABASE).get_table_data('sources')
    destiny = InternalDataBase(DATABASE).get_table_data('destiny')

    def name_source_connection(options):
        return sources.loc[options]['name']
    
    def name_destination_connection(options):
        return destiny.loc[options]['name']
    
    sources_list = list(sources.index) if len(sources) > 0 else {}
    destination_list = list(destiny.index) if len(destiny) > 0 else {}

    idx_source = sources_list.index(conn_params['source']) if conn_params.get('source', None) else None
    idx_destination = destination_list.index(conn_params['destination']) if conn_params.get('destination', None) else None

    conn_name = st.text_input("Insira o nome da conexão", value=conn_params.get('name', ''), placeholder="Nome da conexão")
    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox("Selecione a Fonte de Dados", sources_list, format_func=name_source_connection, index=idx_source, placeholder="Selecionar", )
    with col2:
        destination = st.selectbox("Selecione o Destino de Dados", destination_list, format_func=name_destination_connection, index=idx_destination, placeholder="Selecionar")

    table_name = st.text_input("Escolha um nome para a tabela", value=conn_params.get('table_name', ''), placeholder="Nome da tabela")

    st.title("Importar query para conexão")
    if st.toggle("Code Editor", value=True if conn_params.get('file', None) else False):
        editor = code_editor(conn_params.get('file', ''), lang='sql', buttons=custom_buttons, allow_reset=True)
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
        
        data = [{
            'uuid':conn_id,
            'name':conn_name,
            'source': source, 
            'destination': destination,
            'table_name':table_name,
            'file':query
        }]

        if isinstance(conn_params, pd.Series):
            database.update_data(TABLE, data)
        else:
            database.insert_new_data(TABLE, data)

        st.success(f"{conn_name} criada com sucesso!")
        st.session_state.button_connect_disabled = False
        st.session_state.button_close_disabled = True
        
    if st.session_state.button_close_disabled:
        if st.button("Concluir"):
            st.session_state.button_close_disabled = False
            st.rerun()


# Função para exibir as conexões já estabelecidas
def show_connections(database: InternalDataBase):

    header_container = st.container()
    header_container.header("Conexões Estabelecidas")

    connections = database.get_table_data(TABLE)

    if connections is not None:
        for i, conn in enumerate(connections.index, 0):
            current_connection = connections.loc[conn]

            with st.container(height=78, border=True) as tile:
                src = InternalDataBase(DATABASE).get_table_data('sources').loc[current_connection['source']]
                dest = InternalDataBase(DATABASE).get_table_data('destiny').loc[current_connection['destination']]

                name_conn, logo_1, name_1, arrow, logo_2, name_2, delete_btn, edit_btn, play_btn = st.columns([6,1,4,2,1,4,2,2,2])

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
                with delete_btn:
                    if st.button(label=":material/delete:", key=str(i) + "-delete", use_container_width=True):
                        delete_connection(database, connections, conn)
                with edit_btn:
                    if st.button(label=":material/edit:", key=str(i) + "-edit", use_container_width=True):
                        configure_connection(database, current_connection)
                with play_btn:
                    if st.button(label=":material/play_arrow:", key=str(i) + "-play", use_container_width=True):
                        try:
                            run_processor(database, conn)
                            header_container.success("Extração efetuada com sucesso")
                        except Exception as e:
                            header_container.error("Não foi possível fazer extração")
                            print(e)
                
    else:
        st.info("Nenhuma conexão estabelecida até o momento.")

# Função principal da página de conexões
def show_connections_page():
    database = InternalDataBase(DATABASE)
    
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