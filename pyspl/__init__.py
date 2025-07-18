from typing import List
from .libpsi import Psi
import logging
# 配置日志
# 日志格式选项：
# 1. 使用完整路径 (默认，便于在IDE中直接点击跳转)
log_format_full_path = '%(asctime)s - [%(levelname)s] - [%(pathname)s:%(lineno)d:%(funcName)s] - %(message)s'
# 2. 使用简短文件名 (更简洁)
log_format_short_path = '%(asctime)s - [%(levelname)s] - [%(filename)s:%(lineno)d:%(funcName)s] - %(message)s'

# 选择要使用的日志格式 (切换注释以更改格式)
logging.basicConfig(
    level=logging.INFO,
    # format=log_format_full_path  # 使用完整路径
    format=log_format_short_path  # 使用简短文件名
)
# PSI 类型映射表
PSI_TYPE_MAP = {
    0: "ECDH",  # ECDH PSI
    1: "VOLE"   # VOLE PSI
}

# 曲线类型映射表
CURVE_TYPE_MAP = {
    0: "CURVE_INVALID_TYPE",
    1: "CURVE_25519",
    2: "CURVE_FOURQ",
    3: "CURVE_SM2",
    4: "CURVE_SECP256K1",
    5: "CURVE_25519_ELLIGATOR2"
}

class PSIParty:
    def __init__(self, taskid, role, psi_type=1, curve_type=1, address="localhost:50051", redis="localhost:6379", add_meta={},  sysectbits=112, log_dir=".", log_level=2,
                 log_with_console=True, net_log_switch=False, server_output=True, use_redis=True, connect_wait_time=60000, chl_type='mem'):
        self.taskid = taskid
        self.address = address 
        self.role = role #0:sender 1:receiver
        self.redis = redis
        self.psi_type = psi_type
        self.curve_type = curve_type
        self.sysectbits = sysectbits
        self.log_dir = log_dir
        self.log_level = log_level
        self.net_log_switch = net_log_switch
        self.add_meta = add_meta
        self.log_with_console = log_with_console
        self.server_output = server_output
        self.use_redis = use_redis
        self.chl_type = chl_type # mem or grpc
        
        # 记录 PSI 类型和曲线类型
        psi_type_name = PSI_TYPE_MAP.get(self.psi_type, f"UNKNOWN({self.psi_type})")
        curve_type_name = CURVE_TYPE_MAP.get(self.curve_type, f"UNKNOWN({self.curve_type})")
        logging.info(f"Using PSI type: {psi_type_name} (type_id={self.psi_type}) curve_type={curve_type_name} (type_id={self.curve_type})")
        
        self.psi = Psi(self.role, self.taskid, self.address, self.redis,  self.psi_type, self.curve_type, self.sysectbits, self.log_dir, self.log_level, self.log_with_console, self.net_log_switch, self.server_output, self.use_redis, self.chl_type, connect_wait_time, add_meta)

    def Run(self, role, input:List, fast_mode=True, malicious=False, broadcast_result=True):
        # 获取 PSI 类型名称
        psi_type_name = PSI_TYPE_MAP.get(self.psi_type, f"UNKNOWN({self.psi_type})")
        logging.info(f'Running {psi_type_name} PSI with parameters: taskid={self.taskid}, role={self.role}, address={self.address}, redis={self.redis}')
        logging.info(f'Input size: {len(input)}, fast_mode: {fast_mode}, malicious: {malicious}, broadcast_result: {broadcast_result}')

        try:
            result = self.psi.Run(role, input, fast_mode, malicious, broadcast_result)
            logging.info(f'Finish {psi_type_name} PSI successfully!')
            return result
        except Exception as e:
            logging.error(f'Error during {psi_type_name} PSI: {e}')
            raise  # 重新抛出异常，确保错误不会被吞掉
