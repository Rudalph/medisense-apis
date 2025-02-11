from flask import Flask, request, jsonify
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph


neo4j_url = "neo4j+s://babf3722.databases.neo4j.io"
neo4j_user = "neo4j"
neo4j_password ="6qkA7VWxWKgfO5tJ7Lm2yKew2hVd3X7GBp_5F-93aNI"


graph = Neo4jGraph(neo4j_url, neo4j_user, neo4j_password)
graph.refresh_schema()


def prescription():
    # Get input value from frontend
    input_value = request.json.get('question')
    print(input_value)

    # Construct Cypher query to get generic name for the given brand name
    # cypher_query = f"MATCH (b:Brand {{name: '{input_value}'}})-[:HAS_GENERIC]->(g:Generic) RETURN g.name"
    cypher_query = "MATCH (b:Brand {name: $input_value})-[:HAS_GENERIC_NAME]->(g:GenericName) RETURN g.name AS genericName"
    result = graph.query(cypher_query, params={"input_value": input_value})
    print(result)
    if result:
        generic_name = result[0]['genericName']
        print(generic_name)
        
        # Construct Cypher query to get brand details based on generic name
        cypher_query_details = """
        MATCH (b:Brand)-[:HAS_GENERIC_NAME]->(g:GenericName {name: $generic_name})
        OPTIONAL MATCH (b)-[:PRICED_AT]->(p:Price)
        OPTIONAL MATCH (b)-[:HAS_STRENGTH]->(s:Strength)
        OPTIONAL MATCH (b)-[:PACKAGED_AS]->(pkg:Package)
        OPTIONAL MATCH (b)-[:MANUFACTURED_BY]->(c:Company)
        RETURN b.name AS brandName, 
        g.name AS genericName, 
        p.amount AS price, 
        s.value AS strength, 
        pkg.type AS packageName, 
        c.name AS companyName
        """
        
        result_details = graph.query(cypher_query_details,params={"generic_name": generic_name})
        print(result_details)
        
        return jsonify(result_details)
    else:
        return jsonify({'error': 'Brand not found'}), 404