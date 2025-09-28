import os
import sys
import time
import random
from pyspl import PSIExecute, CreateChannel, PSIType, CurveType

def gaia_channel(role, party_id):
    import sys
    sys.path.append('/cube/algo_cpns/1.5.9.30')
    from lego.model_base import ModelBase
    from lego_common.settings import REDIS
    taskid = "psi_test_taskid"
    chl_type = 'grpc'
    redis_addr = f"tcp://{REDIS['host']}:{REDIS['port']}"
    if REDIS.get('password'):
        redis_addr = f"tcp://{REDIS['password']}@{REDIS['host']}:{REDIS['port']}"

    addr, meta = ModelBase.get_connect_info_by_party_id(party_id)
    print(f'{party_id} addr: {addr}, meta: {meta}')
    ctx=CreateChannel(role, taskid, chl_type, addr, redis_addr,meta)
    return ctx


def generate_test_data(size):
    # 生成随机的 uint128 数据
    # 确保生成的数字在 C++ uint128_t 的范围内
    # 在 Python 中，我们将其限制在 2^64-1 以内，这样可以安全地传递给 C++
    random.seed(0)
    return [str(random.randint(0, 2**64-1)) for _ in range(size)]

def run_vole_psi(role,party_id,psi_type,curve_type,size):
    # 创建 VolePsi 实例
    config_json = f'''{{
        "role": {role},
        "psi_type": {psi_type},
        "curve_type": {curve_type},
        "log_dir": "spllogs/psi.log"
    }}'''
    ctx=gaia_channel(role, party_id)
    
    # 生成测试数据
    input_data = generate_test_data(size)
    
    # 调用 Run 方法并获取结果
    s = time.time()
    result = PSIExecute(ctx, config_json, input_data)
    print(f"Role {role} PSI run 耗时: {time.time() - s}")
    
    # 打印结果
    print(f"Role {role} PSI result count: {len(result)}")
    print(f"Role {role} PSI first 5 results: {result[:5] if len(result) >= 5 else result}")
    return result

if __name__ == '__main__':
    # 运行 0 角色
    role = int(sys.argv[1])
    dst_party_id = sys.argv[2]
    size = int(sys.argv[5])
    print(f"role: {role}; party_id: {dst_party_id}")
    for i in PSIType:
        for j in CurveType:
            if j.value == 0:
                continue
            run_vole_psi(role,dst_party_id,i.value,j.value,size)

