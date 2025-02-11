import requests
from flask import request, jsonify
import pdfplumber
import json
import re
from groq import Groq



groq_api_key="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"




def saviour(structured_data):
    complete_response = ""
    client = Groq(api_key=groq_api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f'''From below attached medical report\n\n {structured_data}  \n\n
                                    I want you to generate a JSON response with keys as Health Parameters and Values as the Numeric value of those Health Parameters
                                    for example consider below format \n\n
                                    "Triglycerides": {{
                                    "Value": 321.0,
                                    "Remark": "High"
                                    }}
                                    \n\n
                                    You have to strictly follow the format. No changes in the naming convention of the format will be entertained. So please stick to specified fromat.
                                    if the remark is not specified use your own knowledge and let the user know if its High, Low or Normal
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



def tabular_summary():
    data = request.json
    file_url = data.get('file_url')
    
    # Step 1: Download the PDF from IPFS
    ipfs_url = file_url
    pdf_response = requests.get(ipfs_url)
    
    # Save the PDF locally
    pdf_file_path = "document.pdf"
    with open(pdf_file_path, 'wb') as file:
        file.write(pdf_response.content)
        print(file_url)
        
    # Step 2: Extract text from the PDF
    data = {}
    with pdfplumber.open(pdf_file_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            # Extract text from each page
            text = page.extract_text()
            # Store text in a structured format
            data[f"Page {i}"] = text
        
    # Step 3: Convert the data into JSON
    structured_data = json.dumps(data, indent=4)
    
    response_text = saviour(structured_data)
    
    # Extract a date from the structured_data
    date_pattern = r'\b\d{2,4}[-/]\d{2}[-/]\d{2,4}\b'  # Matches dates like YYYY-MM-DD, DD-MM-YYYY, etc.
    date_match = re.search(date_pattern, structured_data)
    # Use the first matched date or set to "Unknown" if not found
    extracted_date = date_match.group(0) if date_match else "Unknown"

    # Use regex to extract valid key-value pairs from the response
    pattern = r'"([\w\s\-\/]+)":\s*{\s*"Value":\s*([\d\.]+),\s*"Remark":\s*"([^"]+)"\s*}'
    matches = re.findall(pattern, response_text)

    cleaned_data = {
        "Report Date": extracted_date,  # Add the extracted date at the top
        "Health Parameters": {}         # Initialize the parameters section
    }

    for param, value, remark in matches:
        cleaned_data["Health Parameters"][param] = {
            "Value": float(value),
            "Remark": remark
        }  
        
        
    return jsonify(cleaned_data)