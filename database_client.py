import chromadb
import json
with open('config/database.json') as f:
    config = json.load(f)
CLIENT = chromadb.HttpClient(host=config['host'], port=config['port'])
COLLECTION = CLIENT.get_collection(config['collection'])
def get_collection():
    return COLLECTION
