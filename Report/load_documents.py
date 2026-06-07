# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_groq import ChatGroq
# from langchain_community.vectorstores import Chroma
# from langchain.prompts import PromptTemplate
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# import os
# import shutil



# groq_api_key="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"
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2" )
# llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-8b-instant", temperature=0.5)



# def load_documents():

#     directory = "./Data"
#     persist_dir = "./chroma_db1"

#     # Delete old vector database
#     if os.path.exists(persist_dir):
#         shutil.rmtree(persist_dir)

#     loader = PyPDFDirectoryLoader(directory)   
#     documents = loader.load()


#     text_splitter = CharacterTextSplitter(
#         chunk_size=300,
#         chunk_overlap=200,
#         length_function=len,
#         is_separator_regex=False,
#     )
#     print(text_splitter)
#     pages = loader.load_and_split(text_splitter)
#     vectordb = Chroma.from_documents(pages, embeddings, persist_directory="./chroma_db1")
    

# vectorstore_disk = Chroma(
#     persist_directory="./chroma_db1",
#     embedding_function=embeddings
# )

# retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 5})

# template = """
# You are a helpful AI assistant.
# Answer based on the context provided. 
# context: {context}
# input: {input}
# answer:
# """

# prompt = PromptTemplate.from_template(template)
# combine_docs_chain = create_stuff_documents_chain(llm, prompt)
# retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)


import os
import shutil
import gc

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

GROQ_API_KEY = "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"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.5
)

PERSIST_DIR = "./chroma_db1"
DATA_DIR = "./Data"

retrieval_chain = None


def build_prompt_chain():
    template = """
You are a helpful AI assistant.
Answer based on the context provided.

context: {context}
input: {input}

answer:
"""
    prompt = PromptTemplate.from_template(template)
    return create_stuff_documents_chain(llm, prompt)


def load_documents():
    global retrieval_chain

    # release old chain
    retrieval_chain = None
    gc.collect()

    # delete old chroma db
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR, ignore_errors=True)

    loader = PyPDFDirectoryLoader(DATA_DIR)

    text_splitter = CharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    pages = loader.load_and_split(text_splitter)

    vectordb = Chroma.from_documents(
        documents=pages,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    combine_docs_chain = build_prompt_chain()

    retrieval_chain = create_retrieval_chain(
        retriever,
        combine_docs_chain
    )

    return retrieval_chain


def ask_question(question):
    global retrieval_chain

    if retrieval_chain is None:
        vectorstore_disk = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings
        )

        retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 5})
        combine_docs_chain = build_prompt_chain()

        retrieval_chain = create_retrieval_chain(
            retriever,
            combine_docs_chain
        )

    return retrieval_chain.invoke({"input": question})