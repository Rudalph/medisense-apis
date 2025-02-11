from flask import Flask, request, jsonify
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.summarize import load_summarize_chain




groq_api_key="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"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2" )
llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-8b-instant", temperature=0.5)




def upload_report():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        try:
            # Read file data into memory
            file_data = file.read()

            # Create a temporary file
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_pdf.write(file_data)

            # Close the file to ensure it's written to disk
            temp_pdf.close()

            # Pass the file path to PyPDFLoader
            loader = PyPDFLoader(temp_pdf.name)
            pages = loader.load_and_split()

            
            llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-8b-instant")
            chain = load_summarize_chain(llm, chain_type="stuff")

            result = chain.run(pages)

            return jsonify({'summary': result})
        except Exception as e:
            return jsonify({'error': str(e)})