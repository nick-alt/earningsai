import os
import json
import pygsheets
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough


def Createsummary(settings, query_set):

    load_dotenv()
    Gcredentialpath = os.getenv('PATH_TO_CREDENTIALS') 
    gsheetnr = int(settings.gsheetno)
    gsheetname = settings.gsheetname
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    print("Retrieving...")

    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)

    print(settings)
    
    
    print(gsheetname) 

    print("Testing LLM...")
    query = "how was q1 of alfen?"
    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input = {})


    print("setting up Vectorstore...")
    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings, namespace=companyname)

    print("connect with google...")
    gc = pygsheets.authorize(service_file= Gcredentialpath)
    sheet= gc.open(gsheetname)


    wks = sheet[gsheetnr]
    

    print("creating rag_chain...")
                
    template =  """
    """+ rag_promt+"""

    {context}

    Question: {question}

    Helpful Answer:
    """
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = ( 
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()} 
        | custom_rag_prompt
        | llm
    )



    
    print("creating Summary...")

    #Ausblick



    for x in query_set:
        company = companyname
        query= str(x.content)
        query = query.format(company)
    

        gsheetcell = x.gsheetcell
        res = rag_chain.invoke(query)
        print(res)
        wks.update_value( gsheetcell, res.content)

    return "Summary created"

    #Incomestatement



def askchat(settings, query):
    load_dotenv()
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm

    query= str(query)
    query = query.format(companyname)


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)




    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)

    print(settings.companyname)


    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings, namespace=companyname)



                
    template =  """
    """+ rag_promt+"""

    {context}

    Question: {question}

    Helpful Answer:
    """
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = ( 
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()} 
        | custom_rag_prompt
        | llm
    )


    print(rag_chain)
    print(query)

    res = rag_chain.invoke(query)

    print(res)

    return res

def askchat2(settings, query):
    load_dotenv()
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm
    context = str(""" """)



   

    def fullcontext():
        return context
    query= str(query)
    query = query.format(companyname)


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)




    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)

    print(settings.companyname)


    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings, namespace=companyname)
                
    fullquery =  """Use the following pieces of context to answer the question at the end. If you dont know the answer just say that you dont know it, dont try to make up an answer. If the question is empty just provide a empty string, dont guess. Act as a financial analyst providing concise valuable information to the portfolio manager. pay high attention to thruth of every information in the answer, if you are not sure better leave it out. double check the answer for any false information. """+ query+""" 
    """+ context + """ 
    Question:"""+query+""" 
Helpful answer: """

    


    chain = PromptTemplate.from_template(template=fullquery) | llm
    res = chain.invoke(input = {})

    print(res)

    return res

###def getnamespaces(settings):
    load_dotenv()
    indexname = settings.indexname
 
    embeddings = OpenAIEmbeddings(model= "embeddingmodell")
    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings)
    namespaces =  vectorstore.describe_index_stats()
    
   
    print(namespaces)
###
