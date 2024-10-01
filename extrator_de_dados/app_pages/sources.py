import streamlit as st
from .connectors.config_connectors import connectors

# # Página de configuração de fontes de dados
# @st.dialog("Configuração do Postgres")
# def configure_postgres():
#     #st.header("Configuração do Postgres")

#     # Formulário para configurar dados de conexão do Postgres
#     with st.form("postgres_form"):
#         host = st.text_input("Host", placeholder="ex: localhost")
#         port = st.text_input("Porta", placeholder="ex: 5432")
#         database = st.text_input("Banco de Dados", placeholder="ex: my_database")
#         user = st.text_input("Usuário", placeholder="ex: postgres")
#         password = st.text_input("Senha", type="password")

#         # Botão para submeter o formulário
#         submit_button = st.form_submit_button("Conectar")

#         if submit_button:
#             st.success(f"Conectado ao banco de dados {database} em {host}:{port} com o usuário {user}!")


# # Função para obter o caminho absoluto da imagem
# def get_image_path(image_name):
#     return os.path.join(os.path.dirname(__file__), '../assets', image_name)

# Página principal de seleção da fonte de dados
def show_sources_page():
    st.title("Selecione a Fonte de Dados")

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
    st.info("Novas fontes de dados estarão disponíveis em breve. Continue acompanhando para novas atualizações!")

    st.markdown("""
    #### Fontes configuradas
    Depois de configurar suas fontes de dados, elas aparecerão aqui.
    """)

if __name__ == '__main__':
    show_sources_page()