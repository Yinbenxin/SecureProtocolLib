# SecureProtocolLib (中文)

## 简介

SecureProtocolLib是一个基于[隐语（YACL）](https://github.com/secretflow/yacl)和其他开源库开发的安全协议库，主要提供隐私集合求交（PSI）和隐私信息检索（PIR）功能。该库同时支持C++和Python接口，方便在不同场景下使用。

## 功能特点

- **PSI（隐私集合求交）**：支持多种PSI协议实现，包括基于VOLE的高效PSI协议
- **PIR（隐私信息检索）**：提供高效的PIR协议实现
- **双语言支持**：同时提供C++和Python接口，满足不同开发需求
- **高性能**：基于隐语等高性能密码学库构建，保证协议执行效率
- **安全性**：实现了多种安全级别的协议，满足不同场景的安全需求

## 支持语言

- C++
- Python

## 安装

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/yourusername/SecureProtocolLib.git
cd SecureProtocolLib

# 使用Bazel构建C++库
bazel build //cpp/...

# 构建Python包
python setup.py install
```

### 使用Python包

```bash
pip install pyspl
```

## 使用示例

### C++示例

```cpp
// PSI示例
#include "cpp/psi/psi.h"

// 创建PSI实例并运行
psi::Psi psi_instance(role, taskid, party, redis, sysectbits, psi_type);
std::vector<std::string> result = psi_instance.Run(input_data);
```

### Python示例

```python
# PSI示例
from pyspl import PSIParty

# 创建PSI实例并运行
psi = PSIParty(role, taskid, party, redis, sysectbits, psi_type)
result = psi.Run(input_data)
```

## 依赖

- [PSI (Yet Another Cryptography Library)](https://github.com/secretflow/psi)
- 其他开源密码学库

## 许可证

[Apache License 2.0](LICENSE)