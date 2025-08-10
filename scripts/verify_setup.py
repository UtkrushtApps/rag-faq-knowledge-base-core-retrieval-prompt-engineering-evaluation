import chromadb
COLL = 'faq_rag_chunks'
client = chromadb.HttpClient(host='localhost', port=8000)
coll = client.get_collection(COLL)
print(f"Collection {COLL} now has {coll.count()} records.")
d = coll.get(limit=1)
print("Sample record:", d)
