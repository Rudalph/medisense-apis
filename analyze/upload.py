from flask import request, jsonify
import os
import requests
from analyze.extraction_for_graph import extraction_for_graph
from analyze.graph_database import graph_database 




PINATA_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJmYzU5NmQyNS1kNTNjLTQ5MGItYjViZC0xZWU4MmMwNDk4YjkiLCJlbWFpbCI6ImdvbnNhbHZlc3J1ZGFscGhAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjRmMjc4NzRjYzk1NjRjOWI2ZjliIiwic2NvcGVkS2V5U2VjcmV0IjoiNzMwMzQ5NWMxODY2MmQwMzlmZDY1ZTE5NDU2MzFhNDQzMzNjZWFkOWEwMTY5NjkxY2EwNDFhMGZhMGNkOWMyNiIsImV4cCI6MTc2NTAyOTg0OX0.moW-ebV3O8ZuieNDlbE2a3H4b5v4x5pL_givpV5v8Go"




def upload_to_pinata(filepath, jwt_token):
    """
    Uploads a file to IPFS via Pinata.
    """
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {'Authorization': f'Bearer {jwt_token}'}

    with open(filepath, 'rb') as file:
        response = requests.post(url, files={'file': file}, headers=headers)
        return response.json()
 


def upload():
    """
    Endpoint to handle file upload and pinning to IPFS.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file temporarily
    temp_filepath = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(temp_filepath)

    # Upload to Pinata
    try:
        pinata_response = upload_to_pinata(temp_filepath, PINATA_JWT_TOKEN)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the temporary file
        os.remove(temp_filepath)


    graph_json = ''
    print(pinata_response)
    print(f"pinata_response: {pinata_response}, type: {type(pinata_response)}")
    if isinstance(pinata_response, dict) and 'IpfsHash' in pinata_response:
        ipfs_hash = pinata_response['IpfsHash']
        base_url = "https://gateway.pinata.cloud/ipfs/"
        file_url = f"{base_url}{ipfs_hash}"
        print(f"File URL: {file_url}")
        graph_json = extraction_for_graph(file_url)
    else:
        print("Unexpected response format!")
        
    graph_database(graph_json)   
    return jsonify(pinata_response), 200