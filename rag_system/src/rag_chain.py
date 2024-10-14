from .model_utils import llm
from src.logging_config import logger

def rag_retrieval(vectorstore, query):
    try:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        context = retriever.invoke(query)
        if not context:
            logger.warning(f"No context found for query: {query}")
            return None
        return context
    except Exception as e:
        logger.error(f"Error during retrieval: {str(e)}", exc_info=True)
        return None

def rag_prompt(context, question, template):
    try:
        if context is None:
            # Use a default prompt when no context is available
            default_template = [
                {"role": "system", "content": "You are an AI assistant. Answer the question to the best of your ability based on your general knowledge."},
                {"role": "user", "content": "Question: {question}"}
            ]
            default_template[1]["content"] = default_template[1]["content"].format(question=question)
            messages = default_template
        else:
            template[1]["content"] = template[1]["content"].format(context=context, question=question)
            messages = template
        
        completion = llm.chat.completions.create(
            model="Llama-3.2-1B-Instruct-Q8_0-GGUF",
            messages=messages,
            temperature=7,
        )

        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error during prompt generation: {str(e)}", exc_info=True)
        raise

def rag_chain(query, vectorstore, template):
    try:
        context = rag_retrieval(vectorstore, query)
        response = rag_prompt(context, query, template)
        return context, response
    except Exception as e:
        logger.error(f"Error in RAG chain: {str(e)}", exc_info=True)
        raise