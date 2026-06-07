from langchain_community.graphs import Neo4jGraph
from flask import jsonify




NEO4J_URI="neo4j+s://21cbabd1.databases.neo4j.io"
NEO4J_USERNAME="21cbabd1"
NEO4J_PASSWORD="JS_wZzKRR-B_dyOC__aY7_y43dMkCgKDTzqqJt_CCJA"

graph = Neo4jGraph(
url=NEO4J_URI,
username=NEO4J_USERNAME,
password=NEO4J_PASSWORD,
database="21cbabd1"
)



def overview():
    cypher_query = "MATCH (n) RETURN n"
    result = graph.query(cypher_query)
    return jsonify(result)