import multiprocessing
import random
import logging
import json
from pyspl import LabelPSIExecute, CreateChannel, LabelPSIType, CurveType
import sys
def gaia_channel(role, party_id):
    import sys
    sys.path.append('/cube/algo_cpns/1.5.9')
    from lego.model_base import ModelBase
    from lego_common.settings import REDIS
    taskid = "psi_test_taskid"
    chl_type = 'grpc'
    redis_addr = f"tcp://{REDIS['host']}:{REDIS['port']}"
    if REDIS.get('password'):
        redis_addr = f"tcp://{REDIS['password']}@{REDIS['host']}:{REDIS['port']}"

    addr, meta = ModelBase.get_connect_info_by_party_id(party_id)
    print(f'{party_id} addr: {addr}, meta: {meta}')
    ctx=CreateChannel(role, taskid, chl_type, addr, redis_addr,meta, 60000)
    return ctx


def generate_test_data(size_id, size_label):
    # 生成随机的 uint128 数据
    # 确保生成的数字在 C++ uint128_t 的范围内
    # 在 Python 中，我们将其限制在 2^64-1 以内，这样可以安全地传递给 C++
    random.seed(0)
    id = [str(random.randint(0, 2**64-1)) for _ in range(size_id)]
    item = [(i+ i *0.001) for i in range(size_label)]
    label = [item for _ in range(size_id)]
    return id, label

def run_circuit_psi(role, party_id):
    config_json = f'''{{
        "role": {role},
        "psi_type": {LabelPSIType.CIRCUIT.value},
        "curve_type": {CurveType.CURVE_FOURQ.value},
        "log2_scale_factor": 32,
        "log_dir": "spllogs/circuit.log"
    }}'''
    
    logging.info(f"Python - 角色 {role} 开始初始化 PSIParty")
    logging.info(f"Python - 配置: {config_json}")
    ctx=gaia_channel(role, party_id)

    
    # 生成测试数据
    id, label = generate_test_data(1000,30)
    logging.info(f"Python - 角色 {role} 生成了 {len(id)} 条测试数据")
    
    # 调用 Run 方法并获取结果
    logging.info(f"Python - 角色 {role} 开始运行 PSI")
    result = LabelPSIExecute(ctx, config_json, id, label)
    logging.info(f"Python - 角色 {role} PSI 运行完成，结果数量: {len(result)}")
    
    # 打印结果
    print(f"Role {role} PSI result count: {len(result)}")
    print(f"Role {role} PSI first 5 results: {result[:1] if len(result) >= 5 else result}")
    return result

if __name__ == '__main__':
    # 运行 0 角色
    role = int(sys.argv[1])
    party_id = sys.argv[2]
    print(f"role: {role}; party_id: {party_id}")
    run_circuit_psi(role, party_id)
 