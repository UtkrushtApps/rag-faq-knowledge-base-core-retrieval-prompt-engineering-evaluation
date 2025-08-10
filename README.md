# FAQ Knowledge Base RAG System: Retrieval, Prompting & Evaluation

## Task Overview
This system augments GPT-based responses using a knowledge base of embedded FAQ documents and Chroma DB. The infrastructure (Docker, vector DB, document chunking/embedding) is set up for you. Your goal is to implement the main RAG logic (query encoding, chunk retrieval, prompt construction, result logging) to provide accurate, context-cited, and relevant answers to user queries.

## Guidance
- The current setup causes context dilution, hallucinations, and overshooting model token limits. Your RAG implementation should:
  - Encode user queries using the supplied embedding model for cosine similarity retrieval
  - Configure top-k retrieval appropriately to return only the most relevant FAQ chunks
  - Build GPT prompts with clear citation markers for each retrieved chunk, and a few-shot example to aid grounding
  - Use tiktoken to cap the context window (including system/user/assistant tokens) to stay within the GPT model's context limit (e.g., 4096 tokens)
  - Allow the user to filter FAQs by category (e.g., "billing", "troubleshooting") if specified
  - Log end-to-end response time, number of tokens in context, and retrieval precision@k for spot checks
- Don't change ingestion or Chroma setup. Focus on retrieval accuracy, context assembly, prompt design, and evaluation logging.

## Database Access
- **Container:** `chromadb_faq_rag` (port 8000)
- **Collection:** `faq_rag_chunks`
- Use `config/database.json` for DB connection settings
- Data fields: each chunk has `category`, `faq_id`, `chunk_id`, `content`, and `embedding`
- Scripts for chunking, embedding, and population are already run (see logs in setup if needed)

## Objectives
- Complete `rag_pipeline.py`:
  - Implement efficient cosine-sim vector search in Chroma for top-k chunk retrieval
  - Support optional category filtering during retrieval
  - Build a language model-ready prompt with citation markers (e.g., [1], [2]), system/user/assistant roles, and a representative few-shot example
  - Use tiktoken to keep the prompt plus context under the target GPT context window
  - Track/log latency, token counts, and retrieval precision@k to `logs/eval_metrics.csv`

## How to Verify
- Use the queries in `sample_queries.txt` and your own, run through `rag_pipeline.py`
- Confirm that:
  - Returned answers cite accurately relevant FAQ chunks
  - Responses don't hallucinate or offer unsupported claims
  - Prompt never exceeds context limit (token error is caught pre-generation)
  - Retrieval is fast (<300ms typical), and logs show sensible latency and precision@k values

*All infra is automated. Focus only on retrieval, context-window management, and LLM prompt construction. Consult LangChain and tiktoken docs as needed. Use code comments to explain design choices.*
