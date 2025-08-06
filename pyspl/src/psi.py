from typing import List
from .libpsi import Psi
import logging
import json
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
    def __init__(self, config_json):
        # 验证config_json参数
        if config_json is None:
            raise ValueError("config_json must be provided")
        
        # 输出配置日志
        logging.info(f"PSI Party Config: {config_json}")
        
        # 将配置转换为JSON字符串并直接传递给C++层
        self.psi = Psi(config_json)

    def Run(self, input:List):
        """执行PSI计算"""
        # 记录运行开始信息
        logging.info(f"Input - Input size: {len(input)}, Input First 5: {input[:5]}")            

        try:
            result = self.psi.Run(input)
            logging.info(f"PSI computation completed successfully - "
                        f"Input: {len(input)}, Output: {len(result)}")
            return result
            
        except Exception as e:
            logging.error(f"PSI computation failed - Error: {str(e)}")
            raise  # 重新抛出异常，确保错误不会被吞掉