from typing import List
from .libpsi import Psi
import logging

# PSI 类型映射表
PSI_TYPE_MAP = {
    0: "ECDH",  # ECDH PSI
    1: "VOLE"   # VOLE PSI
}

class PSIParty:
    def __init__(self, taskid, role, party, redis, add_meta={},  psi_type=1, sysectbits=112, log_dir=".", log_level=2,
                 log_with_console=True, net_log_switch=False, server_output=True, use_redis=True, connect_wait_time=60000, chl_type='mem'):
        self.taskid = taskid
        self.party = party #address
        self.role = role #0:sender 1:receiver
        self.redis = redis
        self.sysectbits = sysectbits
        self.log_dir = log_dir
        self.log_level = log_level
        self.psi_type = psi_type
        self.net_log_switch = net_log_switch
        self.add_meta = add_meta
        self.log_with_console = log_with_console
        self.server_output = server_output
        self.use_redis = use_redis
        self.chl_type = chl_type # mem or grpc
        
        # 记录 PSI 类型
        psi_type_name = PSI_TYPE_MAP.get(self.psi_type, f"UNKNOWN({self.psi_type})")
        logging.info(f"Using PSI type: {psi_type_name} (type_id={self.psi_type})")
        
        self.psi = Psi(self.role, self.taskid, self.party, self.redis,  self.psi_type, self.sysectbits, self.log_dir, self.log_level, self.log_with_console, self.net_log_switch, self.server_output, self.use_redis, self.chl_type, connect_wait_time, add_meta)

    def Run(self, role, input:List, fast_mode=True, malicious=False, broadcast_result=True):
        # 获取 PSI 类型名称
        psi_type_name = PSI_TYPE_MAP.get(self.psi_type, f"UNKNOWN({self.psi_type})")
        logging.info(f'Running {psi_type_name} PSI with parameters: taskid={self.taskid}, role={self.role}, party={self.party}, redis={self.redis}')
        logging.info(f'Input size: {len(input)}, fast_mode: {fast_mode}, malicious: {malicious}, broadcast_result: {broadcast_result}')

        try:
            result = self.psi.Run(role, input, fast_mode, malicious, broadcast_result)
            logging.info(f'Finish {psi_type_name} PSI successfully!')
            return result
        except Exception as e:
            logging.error(f'Error during {psi_type_name} PSI: {e}')
            raise  # 重新抛出异常，确保错误不会被吞掉
