import logging
from pyspl.src.psi import PSIParty
from pyspl.src.channel import Channel

# 配置日志
# 日志格式选项：
# 1. 使用完整路径 (默认，便于在IDE中直接点击跳转)
log_format_full_path = '[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)d:%(funcName)s] %(message)s'
# 2. 使用简短文件名 (更简洁)
log_format_short_path = '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s'

# 选择要使用的日志格式 (切换注释以更改格式)
logging.basicConfig(
    level=logging.INFO,
    # format=log_format_full_path  # 使用完整路径
    format=log_format_short_path  # 使用简短文件名
)
    