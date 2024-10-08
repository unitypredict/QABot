# pip install --upgrade -r requirements.txt

import os
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader


os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'your-huggingface-api-key'
os.environ["OPENAI_API_KEY"] = 'your-openai-api-key'

pdf_folder_path = r"..\Sources"
loaders = [PyPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]

documents = []
for loader in loaders:
    documents = documents + loader.load()

# Text Splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

print(len(docs))

embeddings = OpenAIEmbeddings()

db = FAISS.from_documents(docs, embeddings)

db.save_local(r'..\VectorStores')