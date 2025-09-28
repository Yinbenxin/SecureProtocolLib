import sys
from pyspl import KEExecute, CreateChannel, PSIType, CurveType
import logging
def gaia_channel(role, party_id):
    sys.path.append('/cube/algo_cpns/1.5.9.30')
    from lego.model_base import ModelBase
    from lego_common.settings import REDIS
    taskid = "ecdh_ke_taskid"
    chl_type = 'grpc'
    redis_addr = f"tcp://{REDIS['host']}:{REDIS['port']}"
    if REDIS.get('password'):
        redis_addr = f"tcp://{REDIS['password']}@{REDIS['host']}:{REDIS['port']}"

    addr, meta = ModelBase.get_connect_info_by_party_id(party_id)
    print(f'{party_id} addr: {addr}, meta: {meta}')
    ctx=CreateChannel(role, taskid, chl_type, addr, redis_addr,meta)
    return ctx


def run_ecdh_ke(role, party_id, key_exchange_size=10000):
    
    # 创建 VolePsi 实例
    config_json = f'''{{
        "role": {role},
        "psi_type": {PSIType.ECDH.value},
        "curve_type": {CurveType.CURVE_SM2.value},
        "batch_size": 4096,
        "log_dir": "spllogs/ke.log"
    }}'''
    
    logging.info(f"Python - 角色 {role} 开始初始化 ECDHKE")
    logging.info(f"Python - 配置: {config_json}")
    ctx=gaia_channel(role, party_id)  # 初始化通道
    # 生成测试数据
    # 调用 Run 方法并获取结果
    logging.info(f"Python - 角色 {role} 开始运行 ECDHKE")
    result = KEExecute(ctx, config_json, key_exchange_size) # 执行密钥交换
    logging.info(f"Python - 角色 {role} ECDHKE 运行完成，结果数量: {len(result)}")
    
    # 打印结果
    print(f"Role {role} ECDHKE result count: {len(result)}, result: {result[0]}")
    print(f"Role {role} ECDHKE first 5 results: {result[:5] if len(result) >= 5 else result}")
    return result

if __name__ == '__main__':
    logging.info("Python - ECDHKE 测试开始")
    role = int(sys.argv[1])
    dst_party_id = sys.argv[2]
    key_exchange_size = int(sys.argv[3])
    run_ecdh_ke(role, dst_party_id, key_exchange_size)
    logging.info("Python - ECDHKE 测试完成")
