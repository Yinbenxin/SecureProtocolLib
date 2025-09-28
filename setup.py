from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.sdist import sdist
import os
import subprocess
import sys
import shlex
# 安装开发版本
# python setup.py develop

# 构建分发包
# python setup.py sdist bdist_wheel

# 安装
# pip install .
class BazelExtension(Extension):
    """用于从Bazel构建的Python扩展"""
    def __init__(self, name, bazel_target):
        super().__init__(name, sources=[])
        self.bazel_target = bazel_target

class BazelBuildExt(build_ext):
    """使用Bazel构建扩展的自定义构建命令"""
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        if not isinstance(ext, BazelExtension):
            super().build_extension(ext)
            returns

        # 确保输出目录存在
        os.makedirs(self.build_temp, exist_ok=True)
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        os.makedirs(extdir, exist_ok=True)

        # 允许通过环境变量传递额外的 Bazel 参数（例如禁用 OpenMP: --define=omp=off）
        extra_opts = os.environ.get("SPL_BAZEL_OPTS", "")
        extra_args = shlex.split(extra_opts) if extra_opts else []

        # 调用Bazel构建目标
        subprocess.check_call(
            ['bazel', 'build', '--config=linux-release'] + extra_args + [ext.bazel_target],
            cwd=os.path.abspath(os.path.dirname(__file__))
        )

        # 找到构建的.so文件并复制到正确的位置
        bazel_bin_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'bazel-bin', 'pyspl', 'src'
        )
        
        # 根据操作系统确定扩展名
        if sys.platform == 'darwin':
            ext_suffix = '.so'
        elif sys.platform == 'win32':
            ext_suffix = '.pyd'
        else:  # Linux和其他类Unix系统
            ext_suffix = '.so'
            
        # 复制spllib.so到目标目录
        src_file = os.path.join(bazel_bin_dir, 'spllib' + ext_suffix)
        dst_file = os.path.join(extdir, 'src', 'spllib' + ext_suffix)
        
        if os.path.exists(src_file):
            self.copy_file(src_file, dst_file)
        else:
            raise RuntimeError(f"找不到构建的扩展文件: {src_file}")
class CustomSdist(sdist):
    """自定义sdist命令，构建完成后删除tar.gz文件"""
    def run(self):
        # 执行原始的sdist命令
        super().run()
        
        # 删除生成的tar.gz文件
        dist_dir = os.path.join(os.path.dirname(__file__), 'dist')
        tar_gz_file = os.path.join(dist_dir, 'pyspl-0.1.0.tar.gz')
        
        if os.path.exists(tar_gz_file):
            os.remove(tar_gz_file)
            print(f"已删除文件: {tar_gz_file}")

setup(
    name="pyspl",
    version="0.1.0",
    author="Ant Group",
    description="A Python wrapper for Spllib",
    long_description=open("README.md", "r").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # 修改这一行，使用正确的目标名称
    ext_modules=[BazelExtension("pyspl.spllib", "//pyspl/src:spllib_so")],
    cmdclass={
        'build_ext': BazelBuildExt,
        'sdist': CustomSdist,
    },
    install_requires=[
        # 添加依赖项
    ],
)