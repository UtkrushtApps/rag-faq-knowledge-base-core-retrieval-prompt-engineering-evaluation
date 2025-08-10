FROM python:3.9-slim
WORKDIR /srv/app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY scripts /srv/scripts
COPY config /srv/config
ENV PYTHONPATH="/srv/app:/srv/scripts:/srv/config"
