# coding: utf-8
import time
from httpx import AsyncClient
from userAgent import getUserAgent
import re, asyncio


async def get_url(key: str, value: str = '', __expires: int = 0) -> dict:
    host = 'https://wwd.lanzouq.com'
    _id = ''.join(re.findall(r'(?:(?!\/\.com)[^\s])*\b(\S+)', key))
    # print(_id)
    # url = 'https://wwd.lanzouw.com/i43a56d'
    url = f'{host}/tp/{_id}'
    ua = getUserAgent()
    headers = {
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "user-agent": ua,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9",
        'referer': 'https://wwd.lanzouq.com/',
        "cookie": "down_ip=1"
    }
    try:
        async with AsyncClient(
            http2=True,
            headers=headers,
            timeout=10
        ) as http:
            res = await http.get(url=url)
            # print(res.text)
            text = res.text
            title = ''.join(re.findall(r'<title>([\s\S]*?)</title>', res.text))
            url = ''.join(re.findall(r"var spototo = '([\s\S]*?)';", text))
            # print(url)
            _host = ''.join(re.findall(r"var pototo = '([\s\S]*?)';", text)) or 'https://develope.lanzoug.com/file/'
            if value:
                sign = ''.join(re.findall(r"var posign = '([\s\S]*?)';", res.text))
                params = {
                    'action': 'downprocess',
                    'sign': sign,
                    'p': value
                }
                http.headers.update({
                    'content-type': 'application/x-www-form-urlencoded'
                })
                url = f'{host}/ajaxm.php'
                res = await http.post(url=url, data=params)
                data = res.json()
                # print(data)
                url = data.get('url', '')
            url = f'{_host}{url}'
            res = await http.get(url=url)
            url = res.headers.get('location', '')
            url = ''.join(re.findall(r'([\s\S]*?)&b=', url))
            # print(title, url)
            return {
                'title': title,
                'url': url
            }
    except Exception as E:
        print(E)
        return {
            'error': f'{E.args}'
        }


async def xiao_e(b_user_token: str) -> dict:  # 小鹅通 cookie续期
    url = 'https://admin.xiaoe-tech.com/shop_server/user_info'
    ua = getUserAgent()
    headers = {
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "user-agent": ua,
        "origin": "https://admin.xiaoe-tech.com",
        'content-type': 'application/json'
    }
    cookies = {
        'b_user_token': b_user_token
    }
    try:
        async with AsyncClient(
            http2=True,
            headers=headers,
            cookies=cookies,
            timeout=10
        ) as http:
            res = await http.post(url=url)
            print(res.json(), res.headers)
            return {
                'title': '',
                'url': url
            }
    except Exception as E:
        return {
            'error': f'{E.args}'
        }


async def test_url():
    t = time.time()
    url = 'https://store2.lanzoug.com/062709bb/2019/11/02/ddec205dbd15d4b6c502be270ea23527.zip?st=hVhHJDt8ixq9YOCqr3YFFw&e=1656295815'
    ua = getUserAgent()
    headers = {
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "user-agent": ua,
        'Range': 'bytes=1'
    }
    try:
        async with AsyncClient(
            http2=True,
            headers=headers,
            timeout=10
        ) as http:
            for i in range(3000):
                res = await http.get(url=url)
                print('status_code:', res.status_code)
                await asyncio.sleep(30)
                if 416 != res.status_code:
                    break
            print(time.time() - t)
    except Exception as E:
        print(E)
        exit(0)


if __name__ == '__main__':
    # asyncio.run(test_url())
    # asyncio.run(get_url('icSfE07u0aib'))
    # asyncio.run(get_url('i43a56d'))

    asyncio.run(get_url('i74j4rg', '74ou'))
    # asyncio.run(xiao_e('token_62c5193ed46d5JVzwke5jrfyPudHZO8EA'))
    print('11111333'.count('1'))
