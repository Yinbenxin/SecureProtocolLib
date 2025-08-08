from .libpsi import psi_execute as PSIExecute

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