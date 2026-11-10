import asyncio
import time

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.services.external import get_weather, get_rate

router = APIRouter(prefix="/explore", tags=["explore"])


@router.get("")
async def explore(
    city: str = Query(min_length=1),
    currency: str = Query(default="EUR", min_length=3, max_length=3),
):
    start = time.perf_counter()

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            weather, rate = await asyncio.gather(
                get_weather(client, city),
                get_rate(client, currency.upper()),
            )
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="External service is unavailable",
        )

    if weather is None:
        raise HTTPException(status_code=404, detail="City not found")

    if rate is None:
        raise HTTPException(status_code=404, detail="Currency not found")

    return {
        "weather": weather,
        "rate": rate,
        "took_seconds": round(time.perf_counter() - start, 2),
    }