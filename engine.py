import os
import time
import numpy as np
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document
from huggingface_hub import InferenceClient
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "sentence-transformers/all-mpnet-base-v2"
DIMENSION = 768

client = InferenceClient(api_key=HF_TOKEN)

def connect_db():
    if not connections.has_connection("default"):
        # Inside Docker, host will be 'milvus'
        host = os.getenv("MILVUS_HOST", "localhost")
        port = os.getenv("MILVUS_PORT", "19530")
        connections.connect(alias="default", host=host, port=port)
        

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == ".pdf":
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    return text

def ingest_file(file_path):
    connect_db()
    filename = os.path.basename(file_path)
    raw_text = extract_text(file_path)
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(raw_text)

    timestamp = int(time.time())
    coll_name = f"data_{timestamp}"

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
    ]
    schema = CollectionSchema(fields, description=f"Data from {filename}")
    collection = Collection(name=coll_name, schema=schema)

    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 8, "efConstruction": 64}
    }
    collection.create_index(field_name="vector", index_params=index_params)

    # Generate Embeddings
    vectors = client.feature_extraction(chunks, model=MODEL_ID)
    
    # Milvus expects a list of lists for vectors and a list for text
    collection.insert([vectors.tolist(), chunks])
    collection.flush()
    collection.load()
    return coll_name

def query_collection(coll_name, user_query):
    connect_db()
    collection = Collection(coll_name)
    collection.load()

    query_vector = client.feature_extraction(user_query, model=MODEL_ID).tolist()

    results = collection.search(
        data=[query_vector],
        anns_field="vector",
        param={"metric_type": "COSINE", "params": {"ef": 64}},
        limit=3,
        output_fields=["text"]
    )
    
    answers = []
    for hit in results[0]:
        answers.append({
            "score": round(float(hit.distance), 4),
            "text": hit.entity.get('text')
        })
    return answers