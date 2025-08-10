import os
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import re

def chunk_faq_document(txt, max_len=192, overlap=32):
    # Splits on Q/A, maintains overlap & category blocks, returns chunks w/ metadata
    lines = txt.split('\n')
    current_category = None
    current_chunk = []
    metadata = []
    chunks = []
    i = 0
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            continue
        if line.startswith('## '):
            current_category = line[3:].strip()
            continue
        if line.startswith('**Q'):
            if current_chunk:
                chunk = '\n'.join(current_chunk)
                chunks.append({'content': chunk, 'category': current_category, 'start_line': i-len(current_chunk)})
                current_chunk = []
        if line:
            current_chunk.append(line)
        i += 1
    if current_chunk:
        chunks.append({'content': '\n'.join(current_chunk), 'category': current_category, 'start_line': i-len(current_chunk)})
    # Further break long chunks
    out = []
    for c in chunks:
        words = c['content'].split()
        n = 0
        total = len(words)
        chunk_idx = 0
        while n < total:
            text = ' '.join(words[n:n+max_len])
            out.append({'content': text, 'category': c['category'], 'faq_id': f"{c['category']}_{c['start_line']}", 'chunk_id': f"{c['category']}_{c['start_line']}_{chunk_idx}"})
            if n + max_len >= total:
                break
            n += max_len - overlap
            chunk_idx += 1
    return out

if __name__ == "__main__":
    DOC_PATH = '/srv/documents/faqs_expert.txt'
    OUT_PATH = '/srv/data/chunks.jsonl'
    EMB_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
    model = SentenceTransformer(EMB_MODEL)
    print(f"Reading: {DOC_PATH}")
    with open(DOC_PATH, 'r', encoding='utf-8') as fin:
        txt = fin.read()
    all_chunks = chunk_faq_document(txt, max_len=192, overlap=32)
    print(f"Chunked to {len(all_chunks)} sections. Encoding...")
    embs = model.encode([c['content'] for c in all_chunks], show_progress_bar=True, batch_size=32)
    for i, (ch, emb) in enumerate(zip(all_chunks, embs)):
        ch['embedding'] = emb.tolist()
    with open(OUT_PATH, 'w', encoding='utf-8') as fout:
        for chunk in all_chunks:
            fout.write(json.dumps(chunk)+'\n')
    print(f"Processed {len(all_chunks)} chunks.")
