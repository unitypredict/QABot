import os
from unitypredict_engines import ChainedInferenceRequest, ChainedInferenceResponse, FileReceivedObj, FileTransmissionObj, IPlatform, InferenceRequest, InferenceResponse, OutcomeValue
import pickle
import requests
import json 
from typing import Dict
import codecs
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

langchainBot = None

def run_engine(request: InferenceRequest, platform: IPlatform) -> InferenceResponse:
    
    platform.logMsg("Running App Engine...\n")
    # Load environment variables from env.config file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in script directory: {os.listdir(script_dir)}")

    config_file = os.path.join(script_dir, 'env.config')
    if os.path.exists(config_file):
        print(f"Config file {config_file} exists")
        with open(config_file, 'r') as f:
            print(f"Config file contents: {f.read()}")
    else:
        print(f"Config file {config_file} does not exist")

    load_dotenv(config_file)

    # Check if environment variables were loaded
    openai_key = os.getenv('OPENAI_API_KEY')
    hf_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
    print(f"OPENAI_API_KEY loaded: {'Yes' if openai_key else 'No'}")
    print(f"HUGGINGFACEHUB_API_TOKEN loaded: {'Yes' if hf_token else 'No'}")

    engineResponse = InferenceResponse()

    global langchainBot

    if langchainBot == None:
        langchainBot = QAChatBot(platform.getModelsFolderPath())

    inputMsg = request.InputValues['InputMessage']

    context: Dict[str, str] = {}
    if request.Context is not None and len(request.Context.StoredMeta) > 0:
        context = request.Context.StoredMeta

    if "SavedChatHistory" in context:
        storedData = context['SavedChatHistory']
        langchainBot.loadConversationHistory(storedData)
    else:
        langchainBot.chatHistory = {}

    outputMsg = langchainBot.queryModel(inputMsg)

    engineResponse.Outcomes['OutputMessage'] = [OutcomeValue(outputMsg)]

    # save all the meta for next time
    context['SavedChatHistory'] = langchainBot.saveConversationHistory()
    engineResponse.Context.StoredMeta = context


    platform.logMsg("Finished Running App Engine...\n")
    return engineResponse

class QAChatBot:
    model = None
    botEmbeddings = None
    vectorStore = None
    chatHistory = {}
    retriever = None
    contextualize_q_system_prompt = ''
    contextualize_q_prompt = None
    history_aware_retriever = None
    qa_system_prompt = ''
    qa_prompt = None
    question_answer_chain = None
    rag_chain = None
    conversational_rag_chain = None

    def __init__(self, localVectorStoreDirPath):
        # Initialize model and embeddings in constructor
        self.model = ChatOpenAI(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o'), 
            temperature=float(os.getenv('TEMPERATURE', 0))
        )
        self.botEmbeddings = OpenAIEmbeddings()

        self.contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        self.vectorStore = FAISS.load_local(localVectorStoreDirPath, self.botEmbeddings, allow_dangerous_deserialization=True)
        self.retriever = self.vectorStore.as_retriever()


        self.history_aware_retriever = create_history_aware_retriever(
            self.model, self.retriever, self.contextualize_q_prompt
        )

        self.qa_system_prompt = """Use the following pieces of context to answer the user questions. If you don't know the answer, just say that you don't know, don't try to make up an answer. 
            Try to be descriptive and provide as much instructions as possible to guide the user
            {context}"""
        
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.qa_system_prompt),
                MessagesPlaceholder("chat_history", n_messages=5),
                ("human", "{input}"),
            ]
        )
        self.question_answer_chain = create_stuff_documents_chain(self.model, self.qa_prompt)

        self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.question_answer_chain)

        self.conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.chatHistory:
            self.chatHistory[session_id] = ChatMessageHistory()
        return self.chatHistory[session_id]
    
    def queryModel(self, question):
        result = self.conversational_rag_chain.invoke(
            {"input": question},
            config={
                "configurable": {"session_id": "newsession"}
            },
        )["answer"]

        return result
    
    def loadConversationHistory(self, storedData):
        self.chatHistory = pickle.loads(codecs.decode(storedData.encode(), "base64"))

    def saveConversationHistory(self):
        return codecs.encode(pickle.dumps(self.chatHistory), "base64").decode()
