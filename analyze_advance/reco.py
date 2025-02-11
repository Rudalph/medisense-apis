from flask import jsonify
from langchain_community.graphs import Neo4jGraph
from collections import defaultdict
from groq import Groq
import re




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



groq_api_key="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"


def saviour(final_response):
    complete_response = ""
    client = Groq(api_key=groq_api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f'''From below attached data \n\n {final_response}  \n\n
                                    I want you to generate a JSON response specified in below format \n\n
                                    for example consider below format \n\n
                                    {{
                                        Health_parameter_Name : {{
                                                  status : textual content(Is increasing , decreasing or is constant) 
                                                  Recommendations : Textual_Content (with examples)
                                             }}
                                    }}
                                    \n\n
                                    You have to strictly follow the format. No changes in the naming convention of the format will be entertained. So please stick to specified fromat.
                                    
                                    '''
            },
        ],
        temperature=1,
        # max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            complete_response += chunk.choices[0].delta.content
            
    return complete_response





def reco():
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
    
    response_text = saviour(final_response)
    json_regex = r'"([^"]+)":\s*\{\s*"status":\s*"([^"]+)",\s*"Recommendations":\s*"([^"]+)"\s*\}'
    matches = re.findall(json_regex, response_text)
    health_data = {}
    for match in matches:
        param_name, status, recommendations = match
        health_data[param_name] = {
            "status": status,
            "Recommendations": recommendations
        }
        
    return jsonify(health_data)