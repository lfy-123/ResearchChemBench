#!/usr/bin/env python3
"""Authenticated FastAPI gateway for the Stage 03 vLLM service."""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any

import httpx
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request, Response

API_KEY = os.environ.get("STAGE03_LLM_API_KEY", "")
UPSTREAM = os.environ.get("STAGE03_LLM_UPSTREAM", "http://127.0.0.1:18082").rstrip("/")
MAX_CONCURRENCY = max(1, int(os.environ.get("STAGE03_LLM_GATEWAY_CONCURRENCY", "64")))


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=httpx.Timeout(600.0, connect=10.0))
    app.state.slots = asyncio.Semaphore(MAX_CONCURRENCY)
    yield
    await app.state.client.aclose()


app = FastAPI(title="ResearchChemBench Stage 03 LLM", lifespan=lifespan)


def _authorize(authorization: str | None, x_api_key: str | None) -> None:
    supplied = x_api_key or ""
    if authorization and authorization.lower().startswith("bearer "):
        supplied = authorization[7:].strip()
    if API_KEY and supplied != API_KEY:
        raise HTTPException(status_code=401, detail="invalid API key")


@app.get("/health")
async def health() -> dict[str, Any]:
    try:
        response = await app.state.client.get(f"{UPSTREAM}/v1/models", timeout=10.0)
        response.raise_for_status()
        models = response.json().get("data", [])
        return {"status": "ok", "upstream": "ready", "models": len(models)}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"upstream unavailable: {exc}") from exc


@app.api_route("/v1/{path:path}", methods=["GET", "POST"])
async def proxy_v1(
    path: str,
    request: Request,
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None),
) -> Response:
    _authorize(authorization, x_api_key)
    body = await request.body()
    headers = {"content-type": request.headers.get("content-type", "application/json")}
    async with app.state.slots:
        response = await app.state.client.request(
            request.method,
            f"{UPSTREAM}/v1/{path}",
            content=body or None,
            headers=headers,
        )
    forwarded_headers = {
        key: value
        for key, value in response.headers.items()
        if key.lower() in {"content-type", "x-request-id"}
    }
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=forwarded_headers,
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.environ.get("STAGE03_LLM_GATEWAY_HOST", "0.0.0.0"),
        port=int(os.environ.get("STAGE03_LLM_GATEWAY_PORT", "18083")),
        log_level="info",
    )
