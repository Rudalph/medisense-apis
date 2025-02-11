from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain



groq_api_key="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"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2" )
llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-8b-instant", temperature=0.5)



def load_documents():
    directory="./Data"

    loader = PyPDFDirectoryLoader(directory)   
    documents = loader.load()


    text_splitter = CharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    print(text_splitter)
    pages = loader.load_and_split(text_splitter)
    vectordb = Chroma.from_documents(pages, embeddings, persist_directory="./chroma_db1")
    

vectorstore_disk = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 5})

template = """
You are a helpful AI assistant.
Answer based on the context provided. 
context: {context}
input: {input}
answer:
"""

prompt = PromptTemplate.from_template(template)
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)