from math import log
from .spllib import psi_execute as PSIExecute
from .spllib import label_psi_execute 
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
# log2_scale_factor: 对原始数据进行一定放缩，放缩系数为2**log2_scale_factor
def LabelPSIExecute(ctx, config_json, id, label):
    import json
    log2_scale_factor = json.loads(config_json)["log2_scale_factor"]
    scale_factor = 2 ** log2_scale_factor
    # 将label乘以缩放因子并转换为int64
    # label是二维列表，需要对每个子列表中的每个元素进行处理
    scaled_label = [[int(item * scale_factor) for item in sublist] for sublist in label]
    # 执行PSI计算
    result = label_psi_execute(ctx, config_json, id, scaled_label)

    # return result
    # 避免当 scale_factor 为 1 时将大整数转换为 float 导致精度丢失
    if scale_factor == 1:
        scaled_result = [[it for it in sublist] for sublist in result]
    else:
        # 其它情况下使用 Decimal 做精确除法，避免浮点误差
        scaled_result = [[float(Decimal(it) / Decimal(scale_factor)) for it in sublist] for sublist in result]

    return scaled_result
    