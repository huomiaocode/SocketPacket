#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os, re
    
def gen_proto_py():
    proto_path = "./Proto/"
    out_path = "../pbs/"
    files = os.listdir(proto_path)
    for file in files:
        if file.endswith(".proto"):
            cmdStr = "protoc.exe --proto_path=%s --python_out=%s %s%s" % (proto_path, out_path, proto_path, file)
            print(cmdStr)
            os.system(cmdStr)

            file_pb = f"{out_path}/{file.replace('.proto', '_pb2.py')}"
            lines = []
            with open(file_pb, "rb") as f:
                lines = f.read().split(b"\n")
            find_sym_db = False
            find_import = False
            for i in range(len(lines)):
                line = lines[i]
                if line == b"_sym_db = _symbol_database.Default()":
                    find_sym_db = True
                    continue
                if find_sym_db:
                    if not find_import:
                        if line.startswith(b"import "):
                            find_import = True
                            lines[i] = b"from . %s" % line
                    else:
                        if line.startswith(b"import "):
                            lines[i] = b"from . %s" % line
                        else:
                            break
            with open(file_pb, "wb") as f:
                f.write(b"\n".join(lines))
                    

    __init_file = os.path.join(out_path, "__init__.py")
    if not os.path.exists(__init_file):
        with open(__init_file, "w") as f:
            f.write("#")


if __name__ == "__main__":
    os.chdir("protos")
    gen_proto_py()