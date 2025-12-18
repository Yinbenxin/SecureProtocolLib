import multiprocessing
import random
import logging
import time
from pyspl import LabelPSIExecute, CreateChannel, LabelPSIType, CurveType


def generate_test_data(size_id, size_label):
    random.seed(0)
    id = [str(random.randint(0, 2**64-1)) for _ in range(size_id)]
    item = [111 * i for i in range(size_label)]
    label = [item for _ in range(size_id)]
    return id, label


def run_circuit_psi(role, mailbox0, mailbox1, result_dict):
    config_json = f'''{{
        "role": {role},
        "psi_type": {LabelPSIType.CIRCUIT.value},
        "curve_type": {CurveType.CURVE_FOURQ.value},
        "log2_scale_factor": 32,
        "log_dir": "spllogs/circuit.log"
    }}'''

    def send_cb(tag: str, payload: bytes) -> int:
        if role == 0:
            mailbox1[tag] = payload
        else:
            mailbox0[tag] = payload
        return 0

    def recv_cb(tag: str) -> bytes:
        if role == 0:
            while tag not in mailbox0:
                time.sleep(0.001)
            data = mailbox0[tag]
            del mailbox0[tag]
            return data
        else:
            while tag not in mailbox1:
                time.sleep(0.001)
            data = mailbox1[tag]
            del mailbox1[tag]
            return data
    logging.info(f"RCreateChannel")

    ctx = CreateChannel(role, send_cb, recv_cb)
    
    id, label = generate_test_data(1000, 4)
    logging.info(f"Role {role} LabelPSIExecute")

    result = LabelPSIExecute(ctx, config_json, id, label)

    logging.info(f"Role {role} PSI result count: {len(result)}")
    logging.info(f"Role {role} PSI first result: {result[:1] if result else []}")
    result_dict[role] = result


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    manager = multiprocessing.Manager()
    mailbox0 = manager.dict()
    mailbox1 = manager.dict()
    result_dict = manager.dict()

    p0 = multiprocessing.Process(target=run_circuit_psi, args=(0, mailbox0, mailbox1, result_dict))
    p1 = multiprocessing.Process(target=run_circuit_psi, args=(1, mailbox0, mailbox1, result_dict))

    p0.start()
    p1.start()

    p0.join()
    p1.join()

    results = [result_dict.get(0), result_dict.get(1)]

    logging.info("Circuit PSI test completed")
    combined_results = []
    import csv
    if len(results) == 2 and results[0] and results[1]:
        with open('role_0_results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for row in results[0]:
                float_row = [float(item) for item in row]
                writer.writerow(float_row)

        with open('role_1_results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for row in results[1]:
                float_row = [float(item) for item in row]
                writer.writerow(float_row)

        logging.info("Results saved to role_0_results.csv and role_1_results.csv")

        for i in range(len(results[0])):
            for j in range(len(results[0][i])):
                combined_results.append(results[0][i][j] + results[1][i][j])
    else:
        logging.info(f"Results: {results}")
    logging.info(f"Combined results: {combined_results[:20]}")
