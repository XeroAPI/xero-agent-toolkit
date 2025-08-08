FROM python:3.12
WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

COPY . .

USER myuser

ENV PORT=8000
ENV PATH="/home/myuser/.local/bin:$PATH"

EXPOSE $PORT

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]