import httpx

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
NBU_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"


async def get_weather(client: httpx.AsyncClient, city: str) -> dict | None:
    geo = await client.get(GEO_URL, params={"name": city, "count": 1})
    geo.raise_for_status()

    results = geo.json().get("results")
    if not results:
        return None

    place = results[0]

    weather = await client.get(WEATHER_URL, params={
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,wind_speed_10m",
    })
    weather.raise_for_status()

    current = weather.json()["current"]

    return {
        "city": place["name"],
        "country": place.get("country"),
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"],
    }


async def get_rate(client: httpx.AsyncClient, currency: str) -> dict | None:
    response = await client.get(
        NBU_URL,
        params={"valcode": currency, "json": ""},
    )
    response.raise_for_status()

    data = response.json()
    if not data:
        return None

    return {
        "currency": data[0]["cc"],
        "rate_uah": data[0]["rate"],
        "date": data[0]["exchangedate"],
    }