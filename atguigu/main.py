import uvicorn

from atguigu.api.dependencies import init_dialogue_engine
from atguigu.conf.config import settings
from atguigu.utils.db import init_db_engine
from atguigu.utils.httpx_client import init_http_client


def mian():
    init_db_engine()
    init_dialogue_engine()
    init_http_client()
    uvicorn.run('atguigu.api.app:app',
                host=settings.app_host,
                port=settings.app_port,
                )
    # reload=True,


if __name__ == '__main__':
    mian()
