from .embeddings import hf #emebedding model
from langchain_chroma import Chroma # type: ignore

# persist_directory="db"


def vectorstore_init (persist_directory) :
    vectorstore=Chroma(
            persist_directory=persist_directory,
            embedding_function=hf )
    
    return vectorstore

