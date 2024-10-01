import streamlit as st

# Simulando fontes e destinos configurados
# Essas listas podem ser preenchidas dinamicamente conforme você integra com um banco de dados ou armazena essas configurações
configured_sources = [
    {"name": "Postgres - Fonte", "details": {"host": "localhost", "port": 5432, "database": "source_db"}}
]

configured_destinations = [
    {"name": "Postgres - Destino", "details": {"host": "localhost", "port": 5432, "database": "destination_db"}}
]

# Simulando conexões já estabelecidas (você pode armazenar essas informações conforme for estabelecendo as conexões)
connections = []

# Função para configurar uma nova conexão entre Source e Destination
@st.dialog("Configuração de Conexão")
def configure_connection():
    # Se há fontes configuradas, exibir dropdown para seleção
    if configured_sources:
        source = st.selectbox("Selecione a Fonte de Dados", [s["name"] for s in configured_sources])
    else:
        st.warning("Nenhuma fonte de dados configurada ainda.")
        return
    
    # Se há destinos configurados, exibir dropdown para seleção
    if configured_destinations:
        destination = st.selectbox("Selecione o Destino de Dados", [d["name"] for d in configured_destinations])
    else:
        st.warning("Nenhum destino de dados configurado ainda.")
        return

    # Botão para confirmar a conexão
    if st.button("Conectar"):
        connections.append({"source": source, "destination": destination})
        st.success(f"Conexão estabelecida entre {source} e {destination}!")

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
    st.title("Conexões entre Sources e Destinations")
    
    # Seção de configuração de nova conexão
    if st.button("Criar Conexão"):
        configure_connection()
    
    st.markdown("---")
    
    # Seção de visualização das conexões estabelecidas
    show_connections()

if __name__ == '__main__':
    show_connections_page()