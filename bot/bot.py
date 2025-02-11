from flask import Flask, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from flask_cors import CORS
import os
import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from groq import Groq


groq_api_key="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"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2" )
llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-8b-instant", temperature=0.5)


def saviour(req, answer1):
    complete_response = ""
    client = Groq(api_key=groq_api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""The question provided is {req} \n 
                            The generated answer is: {answer1} \n
                            1. If this answer is relevant and correctly addresses the question, return only '1' \n
                            2. If the answer is incorrect, incomplete, or irrelevant, generate a new and correct answer that directly answers the question, but only if the question is related to healthcare.\n
                            3. If the question is not related to healthcare, return: 'I don't know the answer'
                            4. Do not include any additional text beyond what is requested.
                            """
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




# directory="./Data"

# loader = PyPDFDirectoryLoader(directory)   
# documents = loader.load()


# text_splitter = CharacterTextSplitter(
#     separator=".",
#     chunk_size=4000,
#     chunk_overlap=3000,
#     length_function=len,
#     is_separator_regex=False,
# )
# print(text_splitter)
# pages = loader.load_and_split(text_splitter)

# vectordb = Chroma.from_documents(pages, embeddings, persist_directory="./chroma_db")

vectorstore_disk = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 5})

template = """
You are a helpful AI assistant.
Answer only based on the context provided. 
If the question provided to you is out of context just say I don't know.
context: {context}
input: {input}
answer:
"""

prompt = PromptTemplate.from_template(template)
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)


def chat_bot():
    data = request.json
    question = data['question']
    print(question)
    response = retrieval_chain.invoke({"input": question})
    answer1 = response["answer"]
    print("answer1: ",answer1)
    
    answer2 = saviour(question, answer1)
    print("answer2", answer2)
    
    final_answer=""
    
    if answer2.strip()=="1":
        final_answer=answer1
    else:
        final_answer=answer2
    
    print("Final answer: ",final_answer)
    return jsonify({"answer": final_answer})