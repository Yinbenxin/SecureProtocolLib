# python channel_test.py 0 JG0100018800000000 channel_test_task4
# python channel_test.py 1 JG0100018700000000 channel_test_task4

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import time
sys.path.append('/cube/algo_cpns/1.5.9')
from lego.model_base import ModelBase
from lego_common.settings import REDIS
import random
import string

from pyspl import PSIParty
from pyspl import CreateChannel
import logging

def generate_test_data(size):
    """生成测试数据
    
    Args:
        size: 数据大小
        
    Returns:
        生成的随机字符串
    """
    
    # 生成随机字符串
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def channel_test(role, party_id, taskid):
    """Channel通信测试
    
    Args:
        role: 角色 (0: sender, 1: receiver)
        
    Returns:
        测试结果
    """

    # 创建Channel实例
    redis = f"tcp://{REDIS['host']}:{REDIS['port']}"
    if REDIS.get('password'):
        redis = f"tcp://{REDIS['password']}@{REDIS['host']}:{REDIS['port']}"
    address, meta = ModelBase.get_connect_info_by_party_id(party_id)

    logging.info(f'{party_id} redis: {redis}, address: {address}, meta: {meta}')
    logging.info(f"Starting channel test with role {role}")
    # 创建通信通道
    channel = CreateChannel(
        role=role,
        taskid=taskid,
        party=address,
        redis=redis,
        chl_type="grpc",
        meta=meta
    )
    
    result = {}
    
    # 根据角色执行不同操作
    if role == 0:  # sender
        # 生成测试数据
        test_data = generate_test_data(1000000)
        logging.info(f"Sender generated test data: {len(test_data)} bytes")
        
        # 发送数据并统计时间
        start_time = time.time()
        send_success = channel.send(test_data)
        send_time = time.time() - start_time
        
        logging.info(f"Sender sent data, success: {send_success}, time: {send_time:.4f}s")
        
        result = {
            "role": "sender",
            "sent_data_size": len(test_data),
            "send_time_seconds": send_time,
            "success": send_success
        }
        
    else:  # receiver
        # 接收数据并统计时间
        start_time = time.time()
        received_data = channel.recv()
        recv_time = time.time() - start_time
        
        logging.info(f"Receiver got data: {len(received_data)} bytes, time: {recv_time:.4f}s")
        
        result = {
            "role": "receiver",
            "received_data_size": len(received_data),
            "recv_time_seconds": recv_time,
            "success": len(received_data) > 0
        }
    
    return result


if __name__ == "__main__":

    role = int(sys.argv[1])
    dst_party_id = sys.argv[2]
    taskid = sys.argv[3]
    channel_test(role,dst_party_id, taskid)