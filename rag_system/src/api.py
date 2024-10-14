from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.logging_config import logger

app = FastAPI()

class QueryInput(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    context_used: bool

def init_routes(rag_chain, vectorstore, template):
    @app.post("/query", response_model=QueryResponse)
    async def query(input_data: QueryInput):
        try:
            logger.info(f"Received query: {input_data.query}")
            query = input_data.query
            context, response = rag_chain(query, vectorstore, template)
            context_used = context is not None
            logger.info(f"Generated response (context used: {context_used}): {response}")
            return {"response": response, "context_used": context_used}
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}