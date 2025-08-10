import chromadb
import json
CHUNK_PATH = '/srv/data/chunks.jsonl'
COLLECTION = 'faq_rag_chunks'
client = chromadb.HttpClient(host='localhost', port=8000)
with open(CHUNK_PATH, 'r', encoding='utf-8') as f:
    all_chunks = [json.loads(l) for l in f]
if COLLECTION in [c.name for c in client.list_collections()]:
    client.delete_collection(COLLECTION)
coll = client.create_collection(name=COLLECTION)
for i in range(0, len(all_chunks), 50):
    batch = all_chunks[i:i+50]
    ids = [c['chunk_id'] for c in batch]
    docs = [c['content'] for c in batch]
    embs = [c['embedding'] for c in batch]
    metadata = [{k: c[k] for k in c if k not in ['chunk_id', 'content', 'embedding']} for c in batch]
    coll.add(ids=ids, documents=docs, embeddings=embs, metadatas=metadata)
    print(f"Inserted batch {i}-{i+len(batch)-1}")
print("Done populating Chroma DB collection.")
