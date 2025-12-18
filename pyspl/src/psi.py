from math import log

try:
    from .spllib import psi_execute as PSIExecute  # type: ignore[attr-defined]
    from .spllib import label_psi_execute as _label_psi_execute  # type: ignore[attr-defined]
except ModuleNotFoundError:
    try:
        from ..spllib import psi_execute as PSIExecute  # type: ignore[attr-defined]
        from ..spllib import label_psi_execute as _label_psi_execute  # type: ignore[attr-defined]
    except ModuleNotFoundError:
        from pyspl.spllib import psi_execute as PSIExecute  # type: ignore[attr-defined]
        from pyspl.spllib import label_psi_execute as _label_psi_execute  # type: ignore[attr-defined]

from enum import Enum
from decimal import Decimal
import logging
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
    CURVE_25519 = 1 # 25519 通用性更强，互联互通常用
    CURVE_FOURQ = 2 # 4Q 曲线，性能更好
    CURVE_SM2 = 3 # SM2 曲线，国密算法
    CURVE_SECP256K1 = 4 # SECP256K1 曲线，比特币曲线
    CURVE_25519_ELLIGATOR2 = 5 # 25519 曲线，椭圆igator2 编码，防止侧信道攻击
    
    @classmethod
    def get_name(cls, curve_type):
        """获取曲线类型名称"""
        try:
            return cls(curve_type).name
        except ValueError:
            return f"UNKNOWN({curve_type})"

class LabelPSIType(Enum):
    """PSI 算法类型枚举"""
    CIRCUIT = 0  # Circuit PSI
    
    @classmethod
    def get_name(cls, psi_type):
        """获取PSI类型名称"""
        try:
            return cls(psi_type).name
        except ValueError:
            return f"UNKNOWN({psi_type})"
def LabelPSIExecute(ctx, config_json, id, label):
    import json
    log2_scale_factor = json.loads(config_json)["log2_scale_factor"]
    scale_factor = 2 ** log2_scale_factor
    scaled_label = [[int(item * scale_factor) for item in sublist] for sublist in label]
    result = _label_psi_execute(ctx, config_json, id, scaled_label)
    if scale_factor == 1:
        scaled_result = [[it for it in sublist] for sublist in result]
    else:
        scaled_result = [[float(Decimal(it) / Decimal(scale_factor)) for it in sublist] for sublist in result]
    return scaled_result
    
