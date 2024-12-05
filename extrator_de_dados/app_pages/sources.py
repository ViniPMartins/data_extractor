import streamlit as st
import pandas as pd
from .connectors.config_connectors import connectors
from ..utils.database import InternalDataBase

DATABASE = 'internal'
TABLE = 'sources'

@st.dialog("Excluir Conexão")
def delete_connection(database: InternalDataBase, df: pd.DataFrame, id: str):
    conn_name = df.loc[id]['name']
    st.write(f'Digite `{conn_name}` abaixo para deletar a conexão')
    input_name = st.text_input('', label_visibility='hidden')

    if st.button("Deletar"): 
        if conn_name == input_name:
            database.delete_data(TABLE, id)
            st.rerun()
        else:
            st.error('O nome da conexão está incorreto')


# Página principal de seleção da fonte de dados
def show_sources_page():

    database = InternalDataBase(DATABASE)

    st.title("Selecione a Fonte de Dados")

    n_connectors = len(connectors.keys())
    n_rows = int(((3 - (n_connectors%3)) + n_connectors) / 3 if n_connectors % 3 != 0 else n_connectors / 3)

    rows = [st.columns(3) for _ in range(n_rows)]
    
    for idx_row, row in enumerate(rows):
        for idx_col, col in enumerate(row):
            tile = col.container(height=78, border=True)
            id_connector = 3 * idx_row + idx_col
            if id_connector + 1 > n_connectors:
                pass
            else:
                db = connectors[list(connectors.keys())[id_connector]] 
                with tile:
                    sub_col1, sub_col2, sub_col3 = st.columns([3,8,3])
                    with sub_col1:
                        sub_col1.image(db['logo'], width=45)
                    with sub_col2:
                        sub_col2.caption('### ' + db['name'])
                    with sub_col3:
                        if sub_col3.button(label=":heavy_plus_sign:", key=str(id_connector) + "-conf", use_container_width=True):
                            db['config'](database, TABLE)
    
    st.markdown("---")
    st.info("Novas fontes de dados estarão disponíveis em breve. Continue acompanhando para novas atualizações!")

    st.markdown("""
    #### Fontes configuradas
    Depois de configurar suas fontes de dados, elas aparecerão aqui.
    """)

    col1, col2, col3 = st.columns([2,2,8])
    edit = col1.button("Editar Conexão")
    delete = col2.button("Deletar Conexão")

    df = database.get_table_data(TABLE)
    state = st.dataframe(
        df,
        use_container_width=True,
        on_select='rerun',
        selection_mode='single-row'
    )

    if edit:
        r = state['selection']['rows']
        if len(r) == 0:
            st.toast("Selecione uma conexão para editar!")
        else:
            uuid = df.iloc[r].index[0]
            conn = connectors[df['type'].iloc[r[0]]]
            conn['config'](database, TABLE, df.iloc[r[0]], uuid)

    if delete:
        r = state['selection']['rows']
        if len(r) == 0:
            st.toast("Selecione uma conexão para excluir!")
        else:
            uuid = df.iloc[r].index[0]
            delete_connection(database, df, uuid)

if __name__ == '__main__':
    show_sources_page()