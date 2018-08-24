#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os, re
    
def gen_proto_py():
    proto_path = "./Proto/"
    out_path = "../pbs/"
    cmdStr = "protoc.exe --proto_path=%s --python_out=%s %s*.proto" % (proto_path, out_path, proto_path)
    print(cmdStr)
    os.system(cmdStr)
    __init_file = os.path.join(out_path, "__init__.py")
    if not os.path.exists(__init_file):
        with open(__init_file, "w") as f:
            f.write("#")


if __name__ == "__main__":
    os.chdir("protos")
    gen_proto_py()