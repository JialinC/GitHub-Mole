FROM python:3.12.8
WORKDIR /backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y build-essential git netcat-openbsd && \
    git clone https://${GITHUB_TOKEN}@github.com/joshlk/k-means-constrained.git && \
    cd k-means-constrained && \
    pip install .

COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "run.py"]