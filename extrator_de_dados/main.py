import streamlit as st
import os
from .app_pages.sources import show_sources_page
from .app_pages.destinations import show_destination_page
from .app_pages.connections import show_connections_page

# Função principal para o aplicativo Streamlit
def run():
    st.set_page_config(
        page_title="Conector de base de dados",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    pages = [
        st.Page(show_connections_page, title="Connectors", icon=":material/conversion_path:"),
        st.Page(show_sources_page, title="Sources", icon=":material/download:"),
        st.Page(show_destination_page, title="Destinations", icon=":material/upload:")
    ]

    pg = st.navigation(pages)
    pg.run()

# Iniciar o aplicativo Streamlit
if __name__ == "__main__":
    run()