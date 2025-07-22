import multiprocessing
import random
import logging
from pyspl import PSIParty



def generate_test_data(size):
    # 生成随机的 uint128 数据
    # 确保生成的数字在 C++ uint128_t 的范围内
    # 在 Python 中，我们将其限制在 2^64-1 以内，这样可以安全地传递给 C++
    random.seed(0)
    return [str(random.randint(0, 2**64-1)) for _ in range(size)]

def run_vole_psi(role):
    # 创建 VolePsi 实例
    taskid = "taskid"
    address = "localhost:50051"
    redis = "localhost:6379"
    psi_type=0
    curve_type=4
    
    logging.info(f"Python - 角色 {role} 开始初始化 PSIParty")
    logging.info(f"Python - 参数: taskid={taskid}, address={address}, redis={redis}, psi_type={psi_type}, curve_type={curve_type}")
    
    psi = PSIParty(taskid, role, psi_type, curve_type, address, redis)
    
    # 生成测试数据
    input_data = generate_test_data(1000)
    logging.info(f"Python - 角色 {role} 生成了 {len(input_data)} 条测试数据")
    
    # 调用 Run 方法并获取结果
    logging.info(f"Python - 角色 {role} 开始运行 PSI")
    result = psi.Run(role=role, input=input_data, fast_mode=True, malicious=False, broadcast_result=True)
    logging.info(f"Python - 角色 {role} PSI 运行完成，结果数量: {len(result)}")
    
    # 打印结果
    print(f"Role {role} PSI result count: {len(result)}")
    print(f"Role {role} PSI first 5 results: {result[:5] if len(result) >= 5 else result}")
    return result

if __name__ == '__main__':
    logging.info("Python - ECDH PSI 测试开始")
    
    # 创建两个进程，分别运行角色 0 和角色 1
    logging.info("Python - 创建两个进程，分别运行角色 0 和角色 1")
    p0 = multiprocessing.Process(target=run_vole_psi, args=(0,))
    p1 = multiprocessing.Process(target=run_vole_psi, args=(1,))
    
    # 启动进程
    logging.info("Python - 启动进程")
    p0.start()
    p1.start()
    
    # 等待进程结束
    logging.info("Python - 等待进程结束")
    p0.join()
    p1.join()
    
    logging.info("Python - ECDH PSI 测试完成")