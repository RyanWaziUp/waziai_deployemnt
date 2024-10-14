import uvicorn
from src.api import init_routes
from src.rag_chain import rag_chain
from src.vectorstore import vectorstore_init
from src.prompt_templates import template
from src.logging_config import logger

persist_directory = "db"

try:
    logger.info("Initializing vectorstore...")
    vectorstore = vectorstore_init(persist_directory)
    logger.info("Vectorstore initialized successfully.")

    logger.info("Initializing routes...")
    app = init_routes(rag_chain, vectorstore, template)
    logger.info("Routes initialized successfully.")
except Exception as e:
    logger.error(f"Error during initialization: {str(e)}", exc_info=True)
    raise

if __name__ == "__main__":
    logger.info("Starting the server...")
    uvicorn.run(app, host="0.0.0.0", port=8080)