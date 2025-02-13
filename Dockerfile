FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.5.31 /uv /uvx /bin/

ADD . /app
WORKDIR /app

RUN uv sync --frozen
EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "main.py"]
