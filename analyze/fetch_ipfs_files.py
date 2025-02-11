from flask import jsonify
import requests



def fetch_from_pinata(jwt_token):
    url = "https://api.pinata.cloud/data/pinList"
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = requests.get(url, headers=headers)
    return response.json()



def fetch_ipfs_files():
    # Replace with your actual Pinata JWT token
    PINATA_JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJmYzU5NmQyNS1kNTNjLTQ5MGItYjViZC0xZWU4MmMwNDk4YjkiLCJlbWFpbCI6ImdvbnNhbHZlc3J1ZGFscGhAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjRmMjc4NzRjYzk1NjRjOWI2ZjliIiwic2NvcGVkS2V5U2VjcmV0IjoiNzMwMzQ5NWMxODY2MmQwMzlmZDY1ZTE5NDU2MzFhNDQzMzNjZWFkOWEwMTY5NjkxY2EwNDFhMGZhMGNkOWMyNiIsImV4cCI6MTc2NTAyOTg0OX0.moW-ebV3O8ZuieNDlbE2a3H4b5v4x5pL_givpV5v8Go'

    # Fetching data from Pinata API
    data = fetch_from_pinata(PINATA_JWT_TOKEN)

    # Extracting the IPFS pin hashes and file names
   # Extracting the IPFS pin hashes and file names, and filter based on date_unpinned
    files_data = []
    for file in data.get('rows', []):
        # If date_unpinned is None, include it in the response
        if file['date_unpinned'] is None:
            ipfs_hash = file['ipfs_pin_hash']
            file_name = file['metadata']['name']
            file_url = f"https://red-geographical-ox-657.mypinata.cloud/ipfs/{ipfs_hash}"
            files_data.append({'file_name': file_name, 'file_url': file_url})
    
    # Return the extracted data as JSON
    print(files_data)
    return jsonify(files_data)