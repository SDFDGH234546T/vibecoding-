"""
这个模块作用：读取.env文件内容
"""
from pathlib import Path

# 找到.env文件位置 ，当前模块相对位置
ENV_DIR = Path(__file__).parents[2]
ENV_FILE = ENV_DIR / '.env'