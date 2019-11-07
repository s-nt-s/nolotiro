#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import chdir
from os.path import abspath, dirname, isfile

from core.api import NoLoTiro
from core.util import cfg, read, read_tuples, breakline

import re
import sys

abspath = abspath(__file__)
dname = dirname(abspath)
chdir(dname)

msg_template = read("msg.txt")
user, password = cfg(".pw_nolotiro")

done_file = "done.txt"
heavy_file = "heavy.txt"

done = set(read_tuples(done_file)) if isfile(done_file) else set()
heavy = set(read(heavy_file).split("\n")) if isfile(heavy_file) else set()


def reply(t):
    if isfile("msg/"+t.subject+".txt"):
        msg = read("msg/"+t.subject+".txt")
    else:
        mark = "//" if t and t.subject in heavy else "%%"
        msg = re.sub(r"^---.*$", "", msg_template, flags=re.MULTILINE)
        msg = re.sub(r"^"+mark+r" .*$", "", msg, flags=re.MULTILINE)
        msg = re.sub(r"^(%%|//) ", "", msg, flags=re.MULTILINE)
    msg = breakline.sub(r"\n\n", msg)
    if "%s" in msg:
        msg = msg % t.sender
    t.reply(msg)

n = NoLoTiro(user, password)

for t in n.threads():
    if t.key not in done:
        if not t.answered:
            reply(t)
        done.add(t.key)

with open(done_file, "w") as f:
    for d in done:
        f.write("\t".join(d) + "\n")
