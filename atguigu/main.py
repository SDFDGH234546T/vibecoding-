import uvicorn

from atguigu.api.dependencies import init_dialogue_engine
from atguigu.conf.config import settings
from atguigu.utils.db import init_db_engine


def mian():
    init_db_engine()
    init_dialogue_engine()
    uvicorn.run('atguigu.api.app:app',
                host=settings.app_host,
                port=settings.app_port,
                )
    # reload=True,


if __name__ == '__main__':
    mian()
