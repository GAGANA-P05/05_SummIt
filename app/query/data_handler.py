import os
import json
import chromadb
from sentence_transformers import SentenceTransformer

class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Lightweight model
        self.chroma_client = chromadb.PersistentClient(path="chroma_db")  # Persistent storage
        self.collection = self.chroma_client.get_or_create_collection(name="meeting_data")

        # Only initialize embeddings if the database is empty
        if self.collection.count() == 0:
            self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Load meeting data and store embeddings in ChromaDB (only runs once)."""
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            embeddings, metadatas, ids = [], [], []
            for idx, meeting in enumerate(data):
                text_representation = json.dumps(meeting)  # Convert meeting data to text
                vector = self.embedding_model.encode(text_representation).tolist()

                embeddings.append(vector)
                metadatas.append({"meeting": text_representation})
                ids.append(str(idx))

            self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
            print(f"✅ {len(data)} meetings embedded and stored in ChromaDB")

    def get_relevant_data(self, query):
        """Retrieve relevant meeting data using vector search."""
        query_vector = self.embedding_model.encode(query).tolist()
        results = self.collection.query(query_embeddings=[query_vector], n_results=1)

        if results['ids'][0]:  # If a result is found
            return json.loads(results['metadatas'][0][0]['meeting'])
        return None
