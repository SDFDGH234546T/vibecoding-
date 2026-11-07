import uvicorn

from atguigu.conf.config import settings


def mian():
    uvicorn.run('atguigu.api.app:app',
                host=settings.app_host,
                port=settings.app_port)


if __name__ == '__main__':
    mian()
