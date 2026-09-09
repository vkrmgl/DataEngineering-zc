FROM python:3.13.11-slim

WORKDIR /code

RUN pip install uv && \
	uv init && \
	uv add pandas pyarrow

COPY pipeline/pipeline.py .

ENTRYPOINT ["uv", "run", "pipeline.py"]
