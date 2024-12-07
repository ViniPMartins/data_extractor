from .db_engines.config_engines import engines
from ..utils.database import InternalDataBase

TABLE = 'connections'

def run_processor(database: InternalDataBase, connection_id: str):
    
    connections = database.get_table_data(TABLE)
    current_connection = connections.loc[connection_id]

    sources = database.get_table_data('sources')
    destinys = database.get_table_data('destiny')

    current_src = sources.loc[current_connection['source']]
    current_dest = destinys.loc[current_connection['destination']]

    ## Obter tipo e configurações da origem (source)
    source_type = current_src['type']
    source_config = eval(current_src['config'])

    ## Obter tipo e configurações da destino (destination)
    dest_type = current_dest['type']
    dest_config = eval(current_dest['config'])
    
    ## Obter a query
    query = current_connection['file']
    table = current_connection['table_name']

    ## Roda a query no banco de origem -> retorna um dataframe
    source_engine = engines[source_type](source_config)
    result = source_engine.execute_query(query)
    
    # ## Insere os dados no Banco de destino
    dest_engine = engines[dest_type](dest_config)
    dest_engine.insert_data(table, result)

    return True

if __name__ == '__main__':
    run_processor("123")