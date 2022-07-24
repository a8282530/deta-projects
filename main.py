# coding: utf-8
from deta import Deta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
# from addict import Dict
from utils import get_url

async_db = Deta("a0nqnw3h_ijJAWREBqDZVcN2b99RBQfjnVoz3xjmH").AsyncBase("lanzous")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/lanzous/{uid:path}/{pwd:path}")
async def main(uid: str, pwd: str = ''):
    res = await get_url(uid, pwd)
    return res


@app.get("/redirect/{key:path}/{value:path}")
async def redirect(key: str, value: str = ''):
    url = f'https://wwd.lanzouq.com/{key}'
    query = f'{key}|{value}'
    try:
        data = await async_db.get(query)
        # print('data:', dir(data))
        url = data.get('value')
        if url:
            return RedirectResponse(
                url=url,
                status_code=302
            )
    except Exception as _E:
        print(_E)
    try:
        query = {
            "key": key,
            'value': value
        }
        res = await get_url(**query)
        url = res.get('url') or url
        if '?st=' in url:
            await async_db.put_many([{
                'key': f'{key}|{value}',
                'value': url
            }], expire_in=1800)
    except Exception as E:
        print(E)
    return RedirectResponse(
        url=url,
        status_code=302
    )
    # return url

# if __name__ == "__main__":
#     import os
#     command = "uvicorn main:app --host 0.0.0.0 --port 80 --reload"
#     os.system(command)
