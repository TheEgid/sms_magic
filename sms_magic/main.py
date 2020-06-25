import asks
import trio
import os
import contextlib
from dotenv import load_dotenv
import asyncclick as click

from utils import SmscApiError

URL = 'https://smsc.ru/sys/method.php'
JSON_FMT = 3


def get_url(method='send'):
    return URL.replace('method', method)


async def request_smsc(method, login, password, payload):
    """Send request to SMSC.ru service.

    Args:
        method (str): API method. E.g. 'send' or 'status'.
        login (str): Login for account on SMSC.
        password (str): Password for account on SMSC.
        payload (dict): Additional request params, override default ones.
    Returns:
        dict: Response from SMSC API.
    Raises:
        SmscApiError: If SMSC API response status is not 200 or it has `"ERROR" in response.

    Examples:
        >>> request_smsc("send", "my_login", "my_password", {"phones": "+79123456789"})
        {"cnt": 1, "id": 24}
        >>> request_smsc("status", "my_login", "my_password", {"phone": "+79123456789", "id": "24"})
        {'status': 1, 'last_date': '28.12.2019 19:20:22', 'last_timestamp': 1577550022}
    """
    if method not in ['send', 'status']:
        raise SmscApiError(f'unknown {method=}')
    if not payload['phones']:
        raise SmscApiError(f'unknown phones')
    url = get_url(method)
    payload.update({'login': login, 'psw': password, 'fmt': JSON_FMT})
    smsc_response = await asks.get(url, params=payload)
    smsc_response.raise_for_status()
    response = smsc_response.json()
    if 'error' in response:
        raise SmscApiError(response)
    return response



@click.command(load_dotenv())
async def main(**args):
    message = 'Внимание!!, вечером будет шторм!'
    phones = os.getenv("PHONES")
    payload = {'phones': phones, 'mes': message}
    async with trio.open_nursery() as nursery:
        smsc_response = await nursery.start_soon(request_smsc,
                                                 'send',
                                                 os.getenv("LOGIN"),
                                                 os.getenv("PASSWORD"),
                                                 payload)
        print(smsc_response)


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt):
        main(_anyio_backend="trio")




# {'id': 100, 'cnt': 1}
