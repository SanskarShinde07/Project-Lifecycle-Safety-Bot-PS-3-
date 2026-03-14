from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_vector_db():

    loader = DirectoryLoader(
        "data/txt_docs",
        glob="**/*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(documents, embeddings)

    vector_db.save_local("vector_store")

    print("Vector database created successfully")


if __name__ == "__main__":
    create_vector_db()