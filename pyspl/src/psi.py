from typing import List
from .libpsi import Psi
import logging
from enum import Enum

class PSIType(Enum):
    """PSI 算法类型枚举"""
    ECDH = 0  # ECDH PSI
    VOLE = 1  # VOLE PSI
    
    @classmethod
    def get_name(cls, psi_type):
        """获取PSI类型名称"""
        try:
            return cls(psi_type).name
        except ValueError:
            return f"UNKNOWN({psi_type})"

class CurveType(Enum):
    """椭圆曲线类型枚举"""
    CURVE_INVALID_TYPE = 0
    CURVE_25519 = 1
    CURVE_FOURQ = 2
    CURVE_SM2 = 3
    CURVE_SECP256K1 = 4
    CURVE_25519_ELLIGATOR2 = 5
    
    @classmethod
    def get_name(cls, curve_type):
        """获取曲线类型名称"""
        try:
            return cls(curve_type).name
        except ValueError:
            return f"UNKNOWN({curve_type})"

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
        # 获取PSI和曲线类型名称
        psi_type_name = PSIType.get_name(self.psi_type)
        curve_type_name = CurveType.get_name(self.curve_type)
        
        logging.info(f"Initializing PSI Party with all parameters:")
        logging.info(f"  Core Config - Task: {self.taskid}, Role: {self.role}, "
                    f"PSI Type: {psi_type_name} (ID: {self.psi_type}), "
                    f"Curve: {curve_type_name} (ID: {self.curve_type})")
        logging.info(f"  Network Config - Address: {self.address}, Redis: {self.redis}, "
                    f"Channel Type: {self.chl_type}, Use Redis: {self.use_redis}, "
                    f"Connect Wait Time: {connect_wait_time}ms")
        logging.info(f"  Security Config - Security Bits: {self.sysectbits}")
        logging.info(f"  Logging Config - Log Dir: {self.log_dir}, Log Level: {self.log_level}, "
                    f"Console Output: {self.log_with_console}, Network Log: {self.net_log_switch}, "
                    f"Server Output: {self.server_output}")
        logging.info(f"  Additional Metadata: {self.add_meta}")
        
        self.psi = Psi(self.role, self.taskid, self.address, self.redis,  self.psi_type, self.curve_type, self.sysectbits, self.log_dir, self.log_level, self.log_with_console, self.net_log_switch, self.server_output, self.use_redis, self.chl_type, connect_wait_time, add_meta)

    def Run(self, role, input:List, fast_mode=True, malicious=False, broadcast_result=True):
        """执行PSI计算"""
        psi_type_name = PSIType.get_name(self.psi_type)
        input_size = len(input)
        
        # 记录运行开始信息
        logging.info(f"Starting {psi_type_name} PSI computation")
        logging.info(f"Parameters - Task: {self.taskid}, Role: {self.role}, "
                    f"Address: {self.address}, Redis: {self.redis}")
        logging.info(f"Configuration - PSI Type: {psi_type_name}, Fast mode: {fast_mode}, "
                    f"Malicious: {malicious}, Broadcast result: {broadcast_result}")
        logging.info(f"Input - Input size: {input_size}, Input First 5: {input[:5]}")            

        try:
            logging.debug(f"Executing {psi_type_name} PSI algorithm...")
            result = self.psi.Run(role, input, fast_mode, malicious, broadcast_result)
            
            result_size = len(result) if result else 0
            logging.info(f"PSI computation completed successfully - "
                        f"Type: {psi_type_name}, Input: {input_size}, Output: {result_size}")
            return result
            
        except Exception as e:
            logging.error(f"PSI computation failed - Type: {psi_type_name}, "
                         f"Task: {self.taskid}, Error: {str(e)}")
            raise  # 重新抛出异常，确保错误不会被吞掉