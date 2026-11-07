"""
这个模块作用：读取.env文件内容
"""
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 找到.env文件位置 ，当前模块相对位置
ENV_DIR = Path(__file__).parents[2]
ENV_FILE = ENV_DIR / '.env'

# 第一种方式
# os.getenv("key")
# 第二种 pydantic-settings
# 1 创建类，继承pydantic-settings类
class Settings(BaseSettings):
    # 2 调用封装对象读取.env文件内容
    # 到传入.env文件读取内容，把内容读取赋值到对应属性里面
    #* 要求对象起名字，名称必须固定 model_config
    model_config = SettingsConfigDict(
        # env文件位置
        env_file=ENV_FILE,
        # env文件编码
        env_file_encoding='utf-8',
        # 当前类属性数量是否与配置文件一致
        extra='ignore'
    )
    # 不区分大小写
    LLM_MODEL: str
    llm_api_key: str
    llm_base_url: str
    # 数据库
    database_url: str
    # 商城 API
    commerce_api_base_url: str
    # 服务器
    app_host: str
    app_port: int

# 创建Settings对象
settings = Settings()

if __name__ == '__main__':
    print(settings.LLM_MODEL)
    print(settings.llm_api_key)
