from aiohttp import ClientConnectorError
from aiohttp_retry import RetryClient, ExponentialRetry

from exceptions import WeatherException


async def aquery(url: str) -> dict:
    retry_options = ExponentialRetry()
    retry_client = RetryClient(raise_for_status=True, retry_options=retry_options)
    try:
        async with retry_client.get(url) as response:
            data = await response.json()
            return data
    except ClientConnectorError as e:
        raise WeatherException(e)
    finally:
        await retry_client.close()
