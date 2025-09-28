import multiprocessing
import random
import logging
from pyspl import LabelPSIExecute, CreateChannel, LabelPSIType, CurveType



def generate_test_data(size_id, size_label, data):
    random.seed(0)
    id = [str(random.randint(0, 2**64-1)) for _ in range(size_id)]
    item = [data * i for i in range(size_label)]
    label = [item for _ in range(size_id)]
    return id, label

def run_circuit_psi(role):
    config_json = f'''{{
        "role": {role},
        "psi_type": {LabelPSIType.CIRCUIT.value},
        "curve_type": {CurveType.CURVE_FOURQ.value},
        "log2_scale_factor": 32,
        "log_dir": "spllogs/circuit.log"
    }}'''
    ctx = CreateChannel(role, "psi_test", "mem")
    id, label = generate_test_data(1000, 4, role)
    
    result = LabelPSIExecute(ctx, config_json, id, label)
    
    logging.info(f"Role {role} PSI result count: {len(result)}")
    logging.info(f"Role {role} PSI first result: {result[:1] if result else []}")
    return result

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(run_circuit_psi, [0, 1])
    
    logging.info("Circuit PSI test completed")
    
    # 将每方结果保存到CSV文件中
    import csv
    if len(results) == 2 and results[0] and results[1]:
        # 保存角色0的结果
        with open('role_0_results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for row in results[0]:
                # 将每个元素转换为float
                float_row = [float(item) for item in row]
                writer.writerow(float_row)
        
        # 保存角色1的结果
        with open('role_1_results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for row in results[1]:
                # 将每个元素转换为float
                float_row = [float(item) for item in row]
                writer.writerow(float_row)
        
        logging.info("Results saved to role_0_results.csv and role_1_results.csv")
        
        # 将两个结果同位置相加
        combined_results = []
        for i in range(len(results[0])):
            for j in range(len(results[0][i])):
                combined_results.append((results[0][i][j]) + (results[1][i][j]))
    else:
        logging.info(f"Results: {results}")
    logging.info(f"Combined results: {combined_results[:20]}")
    
