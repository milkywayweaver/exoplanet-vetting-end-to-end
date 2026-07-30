FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy\
    UV_NO_DEV=1 \
    UV_TOOL_BIN_DIR=/usr/local/bin \
    MLFLOW_ENABLE_TRACING=false \
    MLFLOW_TRACKING_URI="file:///tmp/mlruns"

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \ 
    uv sync --locked

EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

USER nonroot

CMD ["uv","run","uvicorn","src.app.app:app","--host","0.0.0.0","--port","8000"]