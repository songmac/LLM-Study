
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import os 
from dotenv import load_dotenv

load_dotenv('./credentials/.env') 
api_key = os.environ.get("OPENAI_API_KEY")


#지정된 조건에 따라 주어진 텍스트를 더 작은 덩어리로 분할
def get_text_chunks(text):
    """
    - 텍스트를 통해 청크를 만드는 로직입니다.
    - 청크 사이즈 및 오버랩 등 사용자가 원하는 크기로 청크를 생성합니다.
    """
    text_splitter = RecursiveCharacterTextSplitter(
    separators = "\\n",
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function = len
    )
    chunks = text_splitter.split_text(text)
    
    return chunks


#주어진 텍스트 청크에 대한 임베딩을 생성하고 Chroma를 사용하여 벡터 저장소를 생성
def get_vectorstore(text_chunks):
    """
    - Chroma (Vector DB) 를 생성하는 로직입니다.
    - 청크로 변환된 텍스트를 Chroma 에 넣고 생성합니다.
    - Hugging Face 임베딩을 통해 청크 데이터를 벡터로 변환시킵니다.
    """
    #Hugging Face를 사용한 임베딩
    hf = HuggingFaceEmbeddings(
    model_name='jhgan/ko-sroberta-nli',
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':False},
    )

    #Vector DB 생성
    VectorDB = Chroma.from_texts(text_chunks,
    hf,
    collection_name = "handbook",
    persist_directory = "./db/chromadb"
    )

    return VectorDB

#주어진 벡터 저장소로 대화 체인을 초기화
def get_conversation_chain(vectorstore):
    """
    - Vector DB에 있는 데이터와 사용자 질문(프롬프트)를 함께 OpenAI 에 요청합니다.
    - 받은 결과를 반환합니다.
    """
    memory = ConversationBufferWindowMemory(memory_key='chat_history', return_message=True) #ConversationBufferWindowMemory에 이전 대화 저장
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', api_key=api_key),
        retriever=vectorstore.as_retriever(),
        get_chat_history=lambda h: h,
        memory=memory
    ) #ConversationalRetrievalChain을 통해 langchain 챗봇에 쿼리 전송

    return conversation_chain
