# PSI JSON配置指南

## 概述

为了简化PSI（Private Set Intersection）的参数传递，我们引入了JSON配置功能。现在您可以通过JSON格式来配置所有PSI参数，而不需要传递大量的单独参数。

## 功能特性

- ✅ **简化参数传递**：使用单个JSON对象替代多个参数
- ✅ **向后兼容**：保持原有的参数传递方式
- ✅ **灵活配置**：支持字典、JSON字符串和文件配置
- ✅ **类型安全**：在C++层面进行JSON解析和类型验证
- ✅ **错误处理**：提供详细的配置错误信息

## 使用方法

### 1. 传统参数方式（保持兼容）

```python
from pyspl.src.psi import PSIParty

# 传统方式 - 仍然支持
psi_party = PSIParty(
    taskid="test_task",
    role=0,
    psi_type=1,
    curve_type=1,
    address="localhost:50051",
    redis="localhost:6379",
    # ... 其他参数
)
```

### 2. JSON配置方式

#### 方式A：使用字典配置

```python
config = {
    "taskid": "test_task_001",
    "role": 0,  # 0: sender, 1: receiver
    "psi_type": 1,  # 0: ECDH PSI, 1: VOLE PSI
    "curve_type": 1,  # 1: CURVE_25519, 2: CURVE_FOURQ, etc.
    "address": "localhost:50051",
    "redis": "localhost:6379",
    "sysectbits": 112,
    "log_dir": "./logs",
    "log_level": 2,
    "log_with_console": True,
    "net_log_switch": False,
    "server_output": True,
    "use_redis": True,
    "connect_wait_time": 60000,
    "chl_type": "mem",  # "mem" or "grpc"
    "fast_mode": True,
    "malicious": False,
    "broadcast_result": True,
    "add_meta": {
        "experiment": "test1",
        "version": "1.0"
    }
}

psi_party = PSIParty(config_json=config)
```

#### 方式B：使用JSON字符串

```python
import json

config_str = json.dumps({
    "taskid": "test_task_002",
    "role": 1,
    "psi_type": 0,
    "address": "localhost:50052",
    # ... 其他配置
})

psi_party = PSIParty(config_json=config_str)
```

#### 方式C：从文件读取配置

```python
# 1. 创建配置文件 psi_config.json
{
    "taskid": "production_task",
    "role": 0,
    "psi_type": 1,
    "curve_type": 1,
    "address": "production-server:50051",
    "redis": "redis-cluster:6379",
    "sysectbits": 128,
    "log_dir": "/var/log/psi",
    "log_level": 1,
    "chl_type": "grpc",
    "add_meta": {
        "environment": "production",
        "team": "security"
    }
}

# 2. 从文件加载配置
with open('psi_config.json', 'r') as f:
    config = json.load(f)

psi_party = PSIParty(config_json=config)
```

## 配置参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `taskid` | string | 必需 | 任务ID |
| `role` | int | 必需 | 角色：0=sender, 1=receiver |
| `psi_type` | int | 1 | PSI类型：0=ECDH PSI, 1=VOLE PSI |
| `curve_type` | int | 1 | 曲线类型：1=CURVE_25519, 2=CURVE_FOURQ, 3=CURVE_SM2, 4=CURVE_SECP256K1 |
| `address` | string | "localhost:50051" | 通信地址 |
| `redis` | string | "localhost:6379" | Redis地址 |
| `sysectbits` | int | 112 | 安全参数位数 |
| `log_dir` | string | "." | 日志目录 |
| `log_level` | int | 2 | 日志级别 |
| `log_with_console` | bool | true | 是否输出到控制台 |
| `net_log_switch` | bool | false | 网络日志开关 |
| `server_output` | bool | true | 服务器输出开关 |
| `use_redis` | bool | true | 是否使用Redis |
| `connect_wait_time` | int | 60000 | 连接等待时间(ms) |
| `chl_type` | string | "mem" | 通道类型："mem"或"grpc" |
| `fast_mode` | bool | true | 快速模式 |
| `malicious` | bool | false | 恶意安全模式 |
| `broadcast_result` | bool | true | 是否广播结果 |
| `add_meta` | object | {} | 额外元数据 |

## 技术实现

### Python层面

- 在`PSIParty`类中添加了`config_json`参数
- 支持字典和JSON字符串两种输入格式
- 自动将配置转换为JSON字符串传递给C++层

### C++层面

- 在`Psi`类中添加了JSON构造函数
- 使用`nlohmann/json`库进行JSON解析
- 提供详细的错误处理和日志记录
- 支持默认值和类型验证

### Python绑定

- 在`libpsi.cc`中添加了新的构造函数绑定
- 保持与原有接口的完全兼容性

## 错误处理

当JSON配置格式错误或包含无效值时，系统会抛出详细的错误信息：

```python
try:
    psi_party = PSIParty(config_json=invalid_config)
except Exception as e:
    print(f"配置错误: {e}")
    # 输出: 配置错误: Invalid JSON configuration: ...
```

## 最佳实践

1. **使用配置文件**：对于生产环境，建议使用配置文件管理参数
2. **参数验证**：在传递给PSI之前验证关键参数
3. **环境分离**：为不同环境（开发、测试、生产）使用不同的配置文件
4. **版本控制**：将配置文件纳入版本控制，但注意敏感信息的处理
5. **文档化**：为每个配置参数添加注释说明

## 示例代码

完整的示例代码请参考 `example_json_config.py` 文件，其中包含了各种使用场景的演示。

## 迁移指南

### 从传统方式迁移到JSON配置

1. **识别现有参数**：列出当前使用的所有PSI参数
2. **创建JSON配置**：将参数转换为JSON格式
3. **测试验证**：确保新配置产生相同的行为
4. **逐步迁移**：可以逐个模块进行迁移

### 示例迁移

**迁移前：**
```python
psi = PSIParty(
    taskid="task1",
    role=0,
    psi_type=1,
    address="localhost:50051",
    redis="localhost:6379"
)
```

**迁移后：**
```python
config = {
    "taskid": "task1",
    "role": 0,
    "psi_type": 1,
    "address": "localhost:50051",
    "redis": "localhost:6379"
}
psi = PSIParty(config_json=config)
```

## 常见问题

**Q: JSON配置是否会影响性能？**
A: JSON解析只在初始化时进行一次，对运行时性能没有影响。

**Q: 是否可以混合使用JSON配置和传统参数？**
A: 当前实现中，如果提供了`config_json`，传统参数会被忽略。建议选择一种方式使用。

**Q: 如何处理敏感配置信息？**
A: 建议使用环境变量或专门的密钥管理系统，在运行时动态注入敏感信息。

**Q: JSON配置支持哪些数据类型？**
A: 支持字符串、整数、布尔值和对象（用于meta字段）。

## 更新日志

- **v1.0.0**: 初始版本，支持基本的JSON配置功能
- 添加了Python层面的JSON配置支持
- 添加了C++层面的JSON解析
- 添加了完整的错误处理机制