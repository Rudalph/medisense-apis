import re
from langchain_community.graphs import Neo4jGraph




def graph_database(json_data):
    # Extract the report date
    report_date = json_data.get("Report Date")

    # Initialize the base query
    cypher_query = f'CREATE (r:Report {{report_date: "{report_date}"}})\n'

    # Iterate through health parameters to generate nodes and relationships
    for param_name, param_details in json_data["Health Parameters"].items():
        value = param_details["Value"]
        remark = param_details["Remark"]
        
        # Sanitize parameter name for use as a variable name in Cypher
        sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', param_name)

        # Add the health parameter node
        cypher_query += f'CREATE ({sanitized_name}:HealthParameter {{name: "{param_name}", value: {value}, remark: "{remark}"}})\n'
        
        # Add the relationship
        cypher_query += f'CREATE (r)-[:HAS_PARAMETER]->({sanitized_name})\n'

    
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
    
    query = f"{cypher_query}"
    graph.query(query)