# pip install --upgrade -r requirements.txt

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables from env.config file
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, 'env.config')
load_dotenv(config_file)

# Get configuration from environment variables
pdf_folder_path = os.getenv('SOURCES_PATH', r"..\Sources")
min_chunk_size = int(os.getenv('MIN_CHUNK_SIZE', 100))
breakpoint_threshold_type = os.getenv('BREAKPOINT_THRESHOLD_TYPE', 'percentile')
breakpoint_threshold_amount = int(os.getenv('BREAKPOINT_THRESHOLD_AMOUNT', 95))

loaders = [PyPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]

documents = []
for loader in loaders:
    documents = documents + loader.load()

# Initialize embeddings for SemanticChunker
embeddings = OpenAIEmbeddings()

# Semantic Text Splitter - splits at semantically meaningful boundaries
text_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type=breakpoint_threshold_type,  # Use percentile-based threshold
    breakpoint_threshold_amount=breakpoint_threshold_amount,  # 95th percentile for breakpoint detection
    min_chunk_size=min_chunk_size,  # Minimum chunk size in characters
)

print("Splitting documents using SemanticChunker...")
docs = text_splitter.split_documents(documents)

print(f"Created {len(docs)} semantic chunks")

# Create FAISS vector store
print("Creating FAISS vector store...")
db = FAISS.from_documents(docs, embeddings)

print("Saving vector store...")
vector_store_path = os.getenv('VECTOR_STORE_PATH', r'..\VectorStores')
db.save_local(vector_store_path)
print("Vector store training completed!")