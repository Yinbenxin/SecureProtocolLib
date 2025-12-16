from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.sdist import sdist
import os
import subprocess
import sys

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
            return

        # 确保输出目录存在
        os.makedirs(self.build_temp, exist_ok=True)
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        os.makedirs(extdir, exist_ok=True)

        # 调用Bazel构建目标
        subprocess.check_call(
            ['bazel', 'build', ext.bazel_target],
            cwd=os.path.abspath(os.path.dirname(__file__))
        )

        bazel_bin_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'bazel-bin', 'pyspl', 'src'
        )

        if sys.platform == 'darwin':
            ext_suffix = '.so'
        elif sys.platform == 'win32':
            ext_suffix = '.pyd'
        else:
            ext_suffix = '.so'

        src_file = os.path.join(bazel_bin_dir, 'spllib' + ext_suffix)
        dst_dir = os.path.join(extdir, 'src')
        os.makedirs(dst_dir, exist_ok=True)
        dst_file = os.path.join(dst_dir, 'spllib' + ext_suffix)

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
        tar_gz_file = os.path.join(dist_dir, 'pyspl-0.6.0.tar.gz')
        
        if os.path.exists(tar_gz_file):
            os.remove(tar_gz_file)
            print(f"已删除文件: {tar_gz_file}")

setup(
    name="pyspl",
    version="0.6.0",
    author="Ant Group",
    description="密码算法库",
    long_description=open("README.md", "r").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    ext_modules=[BazelExtension("pyspl.spllib", "//pyspl/src:spllib_so")],
    cmdclass={
        'build_ext': BazelBuildExt,
        'sdist': CustomSdist,
    },
    install_requires=[
        # 添加依赖项
    ],
)
