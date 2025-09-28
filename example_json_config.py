#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：使用JSON配置来初始化PSI
这个示例展示了如何使用JSON配置来简化PSI参数传递
"""

import json
from pyspl.src.psi import PSIParty

def example_traditional_way():
    """传统的参数传递方式"""
    print("=== 传统参数传递方式 ===")
    psi_party = PSIParty(
        taskid="test_task_001",
        role=0,  # 0: sender, 1: receiver
        psi_type=1,  # 1: VOLE PSI
        curve_type=1,  # 1: CURVE_25519
        address="localhost:50051",
        redis="localhost:6379",
        sysectbits=112,
        log_dir="./logs",
        log_level=2,
        log_with_console=True,
        net_log_switch=False,
        server_output=True,
        use_redis=True,
        connect_wait_time=60000,
        chl_type='mem',
        fast_mode=True,
        malicious=False,
        broadcast_result=True,
        add_meta={"experiment": "test1", "version": "1.0"}
    )
    print(f"PSI Party initialized with taskid: {psi_party.taskid}")
    return psi_party

def example_json_config_way():
    """使用JSON配置的方式"""
    print("\n=== JSON配置方式 ===")
    
    # 定义JSON配置
    config = {
        "taskid": "test_task_002",
        "role": 1,  # 0: sender, 1: receiver
        "psi_type": 0,  # 0: ECDH PSI
        "curve_type": 1,  # 1: CURVE_25519
        "address": "localhost:50052",
        "redis": "localhost:6379",
        "sysectbits": 128,
        "log_dir": "./logs",
        "log_level": 1,
        "log_with_console": True,
        "net_log_switch": True,
        "server_output": True,
        "use_redis": True,
        "connect_wait_time": 30000,
        "chl_type": "grpc",
        "fast_mode": False,
        "malicious": True,
        "broadcast_result": False,
        "add_meta": {
            "experiment": "security_test",
            "version": "2.0",
            "researcher": "Alice"
        }
    }
    
    # 方式1：直接传递字典
    psi_party1 = PSIParty(config_json=config)
    print(f"PSI Party 1 initialized with taskid: {psi_party1.taskid}")
    
    # 方式2：传递JSON字符串
    config_str = json.dumps(config, indent=2)
    print(f"\nJSON配置字符串:\n{config_str}")
    
    psi_party2 = PSIParty(config_json=config_str)
    print(f"PSI Party 2 initialized with taskid: {psi_party2.taskid}")
    
    return psi_party1, psi_party2

def example_mixed_config():
    """混合配置方式：JSON配置 + 参数覆盖"""
    print("\n=== 混合配置方式 ===")
    
    # 基础JSON配置
    base_config = {
        "taskid": "base_task",
        "role": 0,
        "psi_type": 1,
        "address": "localhost:50051",
        "redis": "localhost:6379",
        "log_level": 2
    }
    
    # 使用JSON配置，但通过参数覆盖某些值
    # 注意：当前实现中，如果提供了config_json，其他参数会被忽略
    # 这里只是展示概念，实际使用时需要在JSON中包含所有需要的配置
    psi_party = PSIParty(config_json=base_config)
    print(f"Mixed config PSI Party initialized with taskid: {psi_party.taskid}")
    
    return psi_party

def example_config_from_file():
    """从文件读取JSON配置"""
    print("\n=== 从文件读取配置 ===")
    
    # 创建配置文件
    config_file = "psi_config.json"
    config = {
        "taskid": "file_task_001",
        "role": 0,
        "psi_type": 1,
        "curve_type": 1,
        "address": "localhost:50053",
        "redis": "localhost:6379",
        "sysectbits": 112,
        "log_dir": "./logs",
        "log_level": 2,
        "log_with_console": True,
        "net_log_switch": False,
        "server_output": True,
        "use_redis": True,
        "connect_wait_time": 60000,
        "chl_type": "mem",
        "fast_mode": True,
        "malicious": False,
        "broadcast_result": True,
        "add_meta": {
            "source": "config_file",
            "environment": "development"
        }
    }
    
    # 写入配置文件
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"配置已写入文件: {config_file}")
    
    # 从文件读取配置
    with open(config_file, 'r', encoding='utf-8') as f:
        loaded_config = json.load(f)
    
    # 使用加载的配置初始化PSI
    psi_party = PSIParty(config_json=loaded_config)
    print(f"从文件加载的PSI Party initialized with taskid: {psi_party.taskid}")
    
    return psi_party

def main():
    """主函数"""
    print("PSI JSON配置示例")
    print("=" * 50)
    
    try:
        # 示例1：传统方式
        traditional_psi = example_traditional_way()
        
        # 示例2：JSON配置方式
        json_psi1, json_psi2 = example_json_config_way()
        
        # 示例3：混合配置方式
        mixed_psi = example_mixed_config()
        
        # 示例4：从文件读取配置
        file_psi = example_config_from_file()
        
        print("\n=== 配置对比 ===")
        print(f"传统方式 - Role: {traditional_psi.role}, PSI Type: {traditional_psi.psi_type}")
        print(f"JSON方式1 - Role: {json_psi1.role}, PSI Type: {json_psi1.psi_type}")
        print(f"JSON方式2 - Role: {json_psi2.role}, PSI Type: {json_psi2.psi_type}")
        print(f"混合方式 - Role: {mixed_psi.role}, PSI Type: {mixed_psi.psi_type}")
        print(f"文件方式 - Role: {file_psi.role}, PSI Type: {file_psi.psi_type}")
        
        print("\n所有示例执行成功！")
        
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()