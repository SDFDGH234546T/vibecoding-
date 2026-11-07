"""
这个模块目的：发送远程调用，调用中台里面功能接口
"""
import asyncio

from httpx import AsyncClient

## 第一种 使用python内置模块requests
# import requests
# requests.get()

# 异步操作方便
## 第二种 httpx实现
http_client: AsyncClient | None = None

# 创建http_client方法
def init_http_client():
    global http_client
    http_client = AsyncClient(timeout=10.0)

# 关闭http_client方法
async def close_http_client():
    await http_client.aclose()

# 测试方法
async def test():
    init_http_client()
    result = await http_client.get(
        "http://127.0.0.1:18081/orders/A20260408002/status")
    print(result.json())
    await close_http_client()

if __name__ == "__main__":
    asyncio.run(test())