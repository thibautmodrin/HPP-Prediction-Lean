FROM python:3.11-slim

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY artifacts/ ./artifacts/
COPY data/ ./data/
COPY .streamlit/ ./.streamlit/

ENV PORT=80
EXPOSE ${PORT}

CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]
