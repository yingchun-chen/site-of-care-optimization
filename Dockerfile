FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY config ./config


RUN uv sync --frozen --no-install-project && \
    mkdir -p /app/results
ENV PYTHONPATH=/app/src

CMD ["uv", "run", "python", "-m", "siteofshift.main"]