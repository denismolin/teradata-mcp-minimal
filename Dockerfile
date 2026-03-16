FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY server.py .
COPY *.env .

RUN pip install --no-cache-dir -e .

ENV MCP_TRANSPORT=sse
ENV MCP_HOST=0.0.0.0

EXPOSE 8000

CMD ["python", "server.py"]
