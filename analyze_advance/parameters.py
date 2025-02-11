from flask import jsonify
from langchain_community.graphs import Neo4jGraph
from collections import defaultdict



NEO4J_URI='neo4j+s://7de6eab3.databases.neo4j.io'
NEO4J_USERNAME='neo4j'
NEO4J_PASSWORD='6oXiX1VnIBQrjqz0wTCXpV9pc27pZo-eVKzuCOEHeoA'
AURA_INSTANCEID='7de6eab3'
AURA_INSTANCENAME='Instance01'

graph=Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)




def parameters():
    cypher_query = '''MATCH (hp:HealthParameter)
                    WITH 
                        apoc.text.replace(toLower(hp.name), '[^a-z0-9 ]', '') AS normalized_name, 
                        hp.value AS value
                    RETURN 
                        normalized_name AS HealthParameter, 
                        COLLECT(value) AS Values
                    '''
    result = graph.query(cypher_query)
    
    merged_data = defaultdict(list)
    for entry in result:
        normalized_name = entry['HealthParameter'].replace(" ", "").lower()
        merged_data[normalized_name].extend(entry['Values'])
        
    final_response = [
        {'HealthParameter': key, 'Values': values}
        for key, values in merged_data.items()
    ]
    return jsonify(final_response)