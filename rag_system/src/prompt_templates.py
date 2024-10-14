

# template = """You are an AI assistant tasked with answering questions based on the given context. 
#   Use the following pieces of retrieved context to answer the question. If you don't know the answer, don't try to make up an answer.
#   Context: {context}
#   Question: {question}
#   """
# template=[
#     ("system","You are an AI assistant tasked with answering questions based on the given context. Use the following pieces of retrieved context to answer the question. If you don't know the answer, don't try to make up an answer."),
#     ("user","Context: {context} Question: {question}"),
#   ]

template=[
    {"role": "system", "content": "You are an AI assistant tasked with answering questions based on the given context. Use the following pieces of retrieved context to answer the question. If you don't know the answer, don't try to make up an answer."},
    {"role": "user", "content": "Context:{context} Question: {question}"}
  ] 