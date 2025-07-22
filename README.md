<!-- cspell:disable -->
# SecureProtocolLib (中文)

## 简介

SecureProtocolLib是一个基于[隐语（PSI）](https://github.com/secretflow/psi)和其他开源库开发的安全协议库，主要提供隐私集合求交（PSI）和隐私信息检索（PIR）功能。该库同时支持C++和Python接口，方便在不同场景下使用。

## 功能特点

- **PSI（隐私集合求交）**：支持多种PSI协议实现
  - **ECDH PSI**：基于椭圆曲线密码学的PSI实现，支持多种曲线类型
  - **VOLE PSI**：基于向量不经意线性求值的高效PSI协议
- **PIR（隐私信息检索）**：提供高效的PIR协议实现（开发中）
- **双语言支持**：同时提供C++和Python接口，满足不同开发需求
- **高性能**：基于隐语等高性能密码学库构建，保证协议执行效率
- **安全性**：实现了多种安全级别的协议，满足不同场景的安全需求

## 支持语言

- C++
- Python

## 安装

### 依赖项

- Bazel 6.0.0 或更高版本
- Python 3.6 或更高版本
- C++17 兼容的编译器

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/yourusername/SecureProtocolLib.git
cd SecureProtocolLib

# 使用Bazel构建C++库
bazel build //cpp/...

# 构建并安装Python包
python setup.py install

# 或者安装开发版本
python setup.py develop
```

### 使用Python包

```bash
pip install pyspl
```

## 依赖

- [PSI (Private Set Intersection)](https://github.com/secretflow/psi) - 隐语PSI库
- [YACL (Yet Another Cryptography Library)](https://github.com/secretflow/yacl) - 密码学基础库
- [spdlog](https://github.com/gabime/spdlog) - 高性能日志库
- [fmt](https://github.com/fmtlib/fmt) - 格式化库
- [pybind11](https://github.com/pybind/pybind11) - C++/Python绑定库
- [Bazel](https://bazel.build/) - 构建系统


## 许可证

[Apache License 2.0](LICENSE)