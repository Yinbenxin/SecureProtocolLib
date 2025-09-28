

import multiprocessing
import logging
from pyspl import KEExecute, CreateChannel, PSIType, CurveType


def run_ecdh_ke(role):
    # 创建 VolePsi 实例
    config_json = f'''{{
        "role": {role},
        "psi_type": {PSIType.ECDH.value},
        "curve_type": {CurveType.CURVE_SM2.value},
        "batch_size": 4096,
        "log_dir": "spllogs/ke.log"
    }}'''
    key_exchange_size = 8192
    
    logging.info(f"Python - 角色 {role} 开始初始化 ECDHKE")
    logging.info(f"Python - 配置: {config_json}")
    ctx=CreateChannel(role, "ecdhke_test", "mem")
    # 生成测试数据
    # 调用 Run 方法并获取结果
    logging.info(f"Python - 角色 {role} 开始运行 ECDHKE")
    result = KEExecute(ctx, config_json, key_exchange_size)
    logging.info(f"Python - 角色 {role} ECDHKE 运行完成，结果数量: {len(result)}")
    
    # 打印结果
    print(f"Role {role} ECDHKE result count: {len(result)}")
    print(f"Role {role} ECDHKE first 5 results: {result[:5] if len(result) >= 5 else result}")
    return result

if __name__ == '__main__':
    logging.info("Python - ECDHKE 测试开始")
    
    # 创建两个进程，分别运行角色 0 和角色 1
    logging.info("Python - 创建两个进程，分别运行角色 0 和角色 1")
    p0 = multiprocessing.Process(target=run_ecdh_ke, args=(0,))
    p1 = multiprocessing.Process(target=run_ecdh_ke, args=(1,))
    
    # 启动进程
    logging.info("Python - 启动进程")
    p0.start()
    p1.start()
    
    # 等待进程结束
    logging.info("Python - 等待进程结束")
    p0.join()
    p1.join()
    
    logging.info("Python - ECDH PSI 测试完成")