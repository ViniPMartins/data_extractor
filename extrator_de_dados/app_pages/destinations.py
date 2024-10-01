import streamlit as st
from .connectors.config_connectors import connectors

# Página principal de seleção do destino de dados
def show_destination_page():
    st.title("Selecione o Destino dos Dados")

    # Botão com logo do Postgres
    row1 = st.columns(3)
    
    for idx, col in enumerate(row1):
        tile = col.container(height=78, border=True)
        db = connectors[idx]
        with tile:
            sub_col1, sub_col2, sub_col3 = st.columns([2,5,3])
            with sub_col1:
                sub_col1.image(db['logo'], width=45)
            with sub_col2:
                sub_col2.caption('### ' + db['nome'])
            with sub_col2:
                if sub_col3.button(label=":heavy_plus_sign:", key=str(idx) + "-conf", use_container_width=True):
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
