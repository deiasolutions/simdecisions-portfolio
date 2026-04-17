FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY uv.lock .
COPY hivenode/ hivenode/
COPY simdecisions/ simdecisions/
COPY _tools/ _tools/
COPY tests/ tests/

# Install all dependencies from the flat layout.
RUN uv sync

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8420

# Shell-form CMD so ${PORT} gets substituted at runtime from Railway's injected env var.
CMD uvicorn hivenode.main:app --host 0.0.0.0 --port ${PORT:-8420} --log-level info
