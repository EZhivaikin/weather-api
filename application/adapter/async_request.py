import aiohttp as aiohttp


async def async_request(url, method, headers=None, data=None, params=None, timeout=None):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                timeout=timeout
        ) as response:
            result = await response.json()
    return result
