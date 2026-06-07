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

    
    NEO4J_URI="neo4j+s://21cbabd1.databases.neo4j.io"
    NEO4J_USERNAME="21cbabd1"
    NEO4J_PASSWORD="JS_wZzKRR-B_dyOC__aY7_y43dMkCgKDTzqqJt_CCJA"

    graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    database="21cbabd1"
    )
    
    query = f"{cypher_query}"
    graph.query(query)