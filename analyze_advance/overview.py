from langchain_community.graphs import Neo4jGraph
from flask import jsonify




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



def overview():
    cypher_query = "MATCH (n) RETURN n"
    result = graph.query(cypher_query)
    return jsonify(result)