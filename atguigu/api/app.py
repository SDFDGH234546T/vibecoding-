"""
创建fastapi对象
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from atguigu.api.chat_router import chat_router
from atguigu.utils.db import init_db_engine, close_db_engine
from atguigu.utils.httpx_client import init_http_client, close_http_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 数据库使用对象初始化操作
    init_db_engine()
    # 远程调用对象初始化操作
    init_http_client()
    yield
    await close_db_engine()
    await close_http_client()

# app = FastAPI(lifespan=lifespan)

app = FastAPI()
app.include_router(chat_router)