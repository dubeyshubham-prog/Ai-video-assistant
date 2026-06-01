#-------------------->
#REQUIRED LIBRARIES
#-------------------->
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
import os
from dotenv import load_dotenv
load_dotenv()

#-------------------->
#LOAD MODEL OBJECT
#-------------------->
def get_llm():
    return ChatMistralAI(model = "mistral-small-latest",
                         mistral_api_key = os.getenv("MISTRAL_API_KEY"),
                         temperature=0.3)

#-------------------->
'''
WRITE A FUNCTION TO 
SPLIT ENTIRE TRANSCRIPT
INTO SMALL CHUNKS
'''
#-------------------->
def split_transcript(transcript:str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )
    return splitter.split_text(transcript)


#-------------------->
'''
WRITE A FUNCTION TO
SUMMARIZE THE ENTIRE
TRANSCRIPT
'''
#-------------------->
def summarize(transcript:str) -> str:
    llm = get_llm()

    map_prompt = ChatPromptTemplate([
        ('system',"Summarize this portion of a meeting transcript concisely."),
        ('human','{text}'),
    ])

    map_chain = map_prompt | llm | StrOutputParser()
    chunks = split_transcript(transcript)

    chunk_summarizes = [map_chain.invoke({'text':chunk}) for chunk in chunks]

    combined = '\n\n'.join(chunk_summarizes)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system',
                "You are an expert meeting summarizer. Combine these partial summaries "
                "into one final professional meeting summary in bullet points.",
            ),
            (
                'human','{text}'
            ),
        ]
    )

    combined_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{'text':x}) | combined_prompt | llm | StrOutputParser()
    )

    summary =  combined_chain.invoke(combined)
    return summary


#-------------------->
'''
WRITE A FUNCTION TO 
GENERATE TITLE FOR THE
TRANSCRIPT.
'''
#-------------------->
def generate_title(transcript:str) -> str:
    llm = get_llm()

    title_chain = (
        RunnablePassthrough() |  RunnableLambda(lambda x:{"text":x}) |
        ChatPromptTemplate.from_messages([
            (
                "system",
                "Based on the meeting transcript, generate a short professional meeting title "
                "(max 8 words). Only return the title, nothing else.",
            ),
            ("human", "{text}"),
        ])
        |llm
        |StrOutputParser()
    )
    title = title_chain.invoke(transcript[:2000])
    return title






