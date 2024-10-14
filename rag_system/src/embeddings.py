from langchain_community.embeddings import HuggingFaceEmbeddings


model_kwargs = {'device': 'cpu'}
encode_kwargs = {'device': 'cpu', 'batch_size': 32}

    
hf = HuggingFaceEmbeddings(
        model_name='embedding_model',
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )