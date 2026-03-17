🚀 AI Vector Semantic Search System

An AI-powered semantic search web application that retrieves relevant results based on meaning rather than exact keyword matching.
This system uses vector embeddings + similarity search + LLM integration (Groq) to provide intelligent search responses.

---

📌 Project Overview

Traditional search systems rely on keyword matching which often fail to understand user intent.
This project implements vector-based semantic search, where queries and documents are converted into high-dimensional embeddings and compared using similarity metrics.

The system is designed as a real-world AI search engine prototype and can be extended into:

- Legal document search
- Knowledge base assistant
- RAG (Retrieval Augmented Generation) systems
- Enterprise AI search platforms

---

✨ Features

✅ Semantic vector search
✅ Natural language query understanding
✅ LLM response generation using Groq
✅ Flask-based web interface
✅ Docker container support
✅ Environment variable configuration
✅ Modular vector search engine design
✅ Simple UI using HTML templates

---

🧠 System Architecture

User Query
→ Flask Web App
→ Embedding Generation
→ Vector Similarity Search
→ Context Retrieval
→ Groq LLM Response
→ Result Display

---

🏗️ Project Structure

VECTOR_SEARCH_UI/

├── docs/
├── templates/
│   └── index.html

├── app.py
├── engine.py
├── groq.py

├── Dockerfile
├── docker-compose.yml

├── requirements.txt
├── .env
├── .gitignore
└── venv/

---

⚙️ Installation & Setup

1️⃣ Clone Repository

git clone https://github.com/dhanushhpgowda/Vector-search.git
cd Vector-search

2️⃣ Create Virtual Environment

python -m venv venv

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a ".env" file and add:

GROQ_API_KEY=your_api_key_here

5️⃣ Run Application

python app.py

Open browser → http://localhost:5000

---

🐳 Running with Docker

docker-compose up --build

---

🔎 How Vector Search Works

1. Documents are converted into embedding vectors
2. User query is converted into embedding
3. Cosine similarity is calculated
4. Most relevant document chunks are retrieved
5. Retrieved context is sent to LLM
6. LLM generates intelligent final answer

---

🎯 Future Enhancements

- Add FAISS / PGVector for scalable search
- Add authentication system
- Deploy on cloud (AWS / Render / Railway)
- Add chat history memory
- Add hybrid search (keyword + semantic)
- Improve UI with React

---

👨‍💻 Author

Dhanush P Gowda
BE Student | AI & Software Projects