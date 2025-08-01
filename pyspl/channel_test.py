#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing

from pyspl import Channel
import time
import logging

def generate_test_data(size):
    """生成测试数据
    
    Args:
        size: 数据大小
        
    Returns:
        生成的随机字符串
    """
    import random
    import string
    
    # 生成随机字符串
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def channel_test(role):
    """Channel通信测试
    
    Args:
        role: 角色 (0: sender, 1: receiver)
        
    Returns:
        测试结果
    """

    
    # 创建Channel实例
    taskid = "channel_test_task"
    address = "localhost:50051"
    redis = "localhost:6379"
    
    logging.info(f"Starting channel test with role {role}")
    
    # 创建通信通道
    channel = Channel(
        role=role,
        taskid=taskid,
        party=address,
        redis=redis,
        chl_type="mem"
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
    # 配置命令行参数
    # 双进程模式
    print("启动双进程测试模式...")
    # 创建两个进程，分别运行角色 0 和角色 1
    p0 = multiprocessing.Process(target=channel_test, args=(0,))
    p1 = multiprocessing.Process(target=channel_test, args=(1,))
    
    # 启动进程
    p0.start()
    p1.start()
    
    # 等待进程结束
    p0.join()
    p1.join()
    print("双进程测试完成")
    