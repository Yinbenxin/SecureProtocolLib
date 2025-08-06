# pip install --no-cache-dir --extra-index-url http://devpiread:Devpiread123@10.12.0.78:13141/root/release/+simple/ --trusted-host 10.12.0.78  pyspl==0.1.0

# PSI_TYPE_MAP = {
#     0: "ECDH",  # ECDH PSI
#     1: "VOLE"   # VOLE PSI
# }

# # 曲线类型映射表
# CURVE_TYPE_MAP = {
#     0: "CURVE_INVALID_TYPE",
#     1: "CURVE_25519",
#     2: "CURVE_FOURQ",
#     3: "CURVE_SM2",
#     4: "CURVE_SECP256K1",
#     5: "CURVE_25519_ELLIGATOR2"
# }



# python test_vole_psi.py 0 JG0100021700000000 1 2 10000

# python test_vole_psi.py 1 JG0100021600000000 1 2 10000

import os
import sys
import time
sys.path.append('/cube/algo_cpns/1.5.9.30')
from lego.model_base import ModelBase
from lego_common.settings import REDIS
import random
from pyspl import PSIParty

def generate_test_data(size):
    # 生成随机的 uint128 数据
    # 确保生成的数字在 C++ uint128_t 的范围内
    # 在 Python 中，我们将其限制在 2^64-1 以内，这样可以安全地传递给 C++
    random.seed(0)
    return [str(random.randint(0, 2**64-1)) for _ in range(size)]

def run_vole_psi(role,party_id,psi_type,curve_type,size):
    # 创建 VolePsi 实例
    taskid = "taskid"
    chl_type = 'grpc'
    redis_addr = f"tcp://{REDIS['host']}:{REDIS['port']}"
    if REDIS.get('password'):
        redis_addr = f"tcp://{REDIS['password']}@{REDIS['host']}:{REDIS['port']}"

    addr, meta = ModelBase.get_connect_info_by_party_id(party_id)
    print(f'{party_id} addr: {addr}, meta: {meta}')

    psi = PSIParty(taskid=taskid, role=role, psi_type=psi_type, curve_type=curve_type, address=addr, redis=redis_addr, add_meta=meta, chl_type=chl_type)
    
    # 生成测试数据
    input_data = generate_test_data(size)
    
    # 调用 Run 方法并获取结果
    s = time.time()
    result = psi.Run(role=role, input=input_data, fast_mode=True, malicious=False, broadcast_result=True)
    print(f"求交 psi run 耗时: {time.time() - s}")
    
    # 打印结果
    print(f"Role {role} PSI result count: {len(result)}")
    print(f"Role {role} PSI first 5 results: {result[:5] if len(result) >= 5 else result}")
    return result

if __name__ == '__main__':
    # 运行 0 角色
    role = int(sys.argv[1])
    dst_party_id = sys.argv[2]
    psi_type = int(sys.argv[3])
    curve_type = int(sys.argv[4])
    size = int(sys.argv[5])
    print(f"role: {role}; party_id: {dst_party_id}")
    run_vole_psi(role,dst_party_id,psi_type,curve_type,size)

