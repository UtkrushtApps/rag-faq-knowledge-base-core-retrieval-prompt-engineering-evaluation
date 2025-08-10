#!/bin/bash
set -e
if ! docker ps | grep -q chromadb_faq_rag; then
  echo "Starting Chroma DB via docker-compose..."
  docker-compose up -d
else
  echo "Chroma DB container already running."
fi
sleep 7
echo "Processing and embedding FAQ documents..."
docker exec chromadb_faq_rag python3 /srv/scripts/process_documents.py
echo "Populating Chroma DB with FAQ chunks embeddings..."
docker exec chromadb_faq_rag python3 /srv/scripts/populate_database.py
echo "Verifying setup..."
docker exec chromadb_faq_rag python3 /srv/scripts/verify_setup.py
echo "Setup complete.\n"
