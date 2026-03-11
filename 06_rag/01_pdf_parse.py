from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from pathlib import Path

load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"

#Load the file
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

#split the docs into small chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks = text_splitter.split_documents(documents=docs)

#vector embeddings
embedding_model = OpenAIEmbeddings(
    model = "text-embedding-3-small"
)

vector_store = QdrantVectorStore.from_documents(
    documents = chunks,
    embedding = embedding_model,
    url = "http://localhost:6333",
    collection_name = "Learning RAG"
)

print("Indexing of documents done ✅")