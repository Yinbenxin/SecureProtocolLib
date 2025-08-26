load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")
def deps():
    _psi()

def _psi():
    maybe(
        http_archive,
        name = "psi",
        urls = [
                "https://github.com/Yinbenxin/psi/archive/refs/tags/gaia_2.3.tar.gz",
        ],
        strip_prefix = "psi-gaia_2.3",
        sha256 = "af87eb40613315617846cf98554fff71e0e4f5fe67b797a49aebf2c5f4f1fc12",
    )