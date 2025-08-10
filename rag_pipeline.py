"""
FAQ RAG Pipeline - Implement core retrieval, prompt construction, and evaluation metrics.
Fill in these functions for query encoding, vector retrieval, context assembly, prompt crafting (with citations & few-shot), token budgeting, and performance logging.
"""
from sentence_transformers import SentenceTransformer
import tiktoken
import time
import pandas as pd
from database_client import get_collection
MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
COLL = get_collection()
ENCODER = tiktoken.encoding_for_model("gpt-3.5-turbo")

# --- Functions you must implement ---
def encode_query(query):
    """Encode user query using same embedding model (returns np.ndarray)"""
    # TODO: Implement
    pass

def retrieve_chunks(query_vec, top_k=5, category=None):
    """Vector search (cosine) for top_k FAQ chunks, optionally filter by category"""
    # TODO: Implement
    pass

def build_prompt(user_query, chunks, max_tokens=4096):
    """Builds prompt for GPT with citation markers and a single few-shot (template provided), budgets with tiktoken so prompt+context <= max_tokens"""
    # TODO: Implement
    pass

def log_metrics(latency_ms, used_tokens, retrieved_chunks, relevant_ids, log_path='logs/eval_metrics.csv'):
    """Append evaluation metrics to CSV: lat(ms), tokens, precision@k given relevant_ids (hits in top_k)"""
    # TODO: Implement
    pass

# """EXAMPLE usage (not a solution):
# query_vec = encode_query("How do I update my billing address?")
# chunks = retrieve_chunks(query_vec, top_k=5, category="billing")
# prompt = build_prompt("How do I update my billing address?", chunks, max_tokens=4096)
# [run LLM with prompt...]
# log_metrics(lat_total, used_tokens, chunks, [relevant_id1])
# """
