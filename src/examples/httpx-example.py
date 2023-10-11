import asyncio
import httpx


async def make_http2_request(url):
    try:
        async with httpx.AsyncClient(http2=True, verify=False) as client:
            response = await client.get(url)
        return response
    except httpx.RequestError as e:
        print(f'[!] error occurred while making the request: {e}')
        return None


def main():
    url = 'https://localhost/'

    response = asyncio.run(make_http2_request(url))

    print('Response object type:', type(response))
    print('Response HTTP version:', response.http_version)
    print('Response headers:', response.headers)


if __name__ == '__main__':
    main()