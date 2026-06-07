from flask import jsonify
from langchain_community.graphs import Neo4jGraph
from collections import defaultdict



NEO4J_URI="neo4j+s://21cbabd1.databases.neo4j.io"
NEO4J_USERNAME="21cbabd1"
NEO4J_PASSWORD="JS_wZzKRR-B_dyOC__aY7_y43dMkCgKDTzqqJt_CCJA"

graph = Neo4jGraph(
url=NEO4J_URI,
username=NEO4J_USERNAME,
password=NEO4J_PASSWORD,
database="21cbabd1"
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