import streamlit as st
from .connectors.config_connectors import connectors

# Página principal de seleção do destino de dados
def show_destination_page():
    st.title("Selecione o Destino dos Dados")

    # Botão com logo do Postgres
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
                db = connectors[id_connector]
                with tile:
                    sub_col1, sub_col2, sub_col3 = st.columns([2,5,3])
                    with sub_col1:
                        sub_col1.image(db['logo'], width=45)
                    with sub_col2:
                        sub_col2.caption('### ' + db['nome'])
                    with sub_col2:
                        if sub_col3.button(label=":heavy_plus_sign:", key=str(id_connector) + "-conf", use_container_width=True):
                            db['config']()

    # Informações adicionais
    st.markdown("---")
    st.info("Novos destinos de dados estarão disponíveis em breve. Continue acompanhando para novas atualizações!")

    st.markdown("""
    #### Destinos de dados configurados
    Depois de configurar suas fontes de dados, elas aparecerão aqui.
    """)


if __name__ == '__main__':
    show_destination_page()
