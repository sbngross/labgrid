#!/use/bin/python3

import tomlkit
import sys
from io import IOBase

INPUT = "pyproject.toml"


def dump_reqs(out: IOBase, data: dict):
    for r in data["project"]["dependencies"]:
        out.write("%s\n" % r)


with open(INPUT, "r") as f:
    data = tomlkit.load(f)

if len(sys.argv) > 1:
    with open(sys.argv[1], "w") as f:
        dump_reqs(f, data)
else:
    dump_reqs(sys.stdout, data)
