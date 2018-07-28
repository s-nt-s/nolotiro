from core.api import NoLoTiro
from core.util import cfg, read, read_tuples
from os.path import isfile

msg_template = read("msg.txt")
user, password = cfg(".pw_nolotiro")

done_file = "done.txt"

done = set(read_tuples(done_file)) if isfile(done_file) else set()

def reply(t):
    t.reply(msg_template % (t.sender))

n = NoLoTiro(user, password)

for t in n.threads():
    if t.key not in done:
        if t.unread and not t.answered:
            reply(t)
        done.add(t.key)

with open(done_file, "w") as f:
    for d in done:
        f.write("\t".join(d)+"\n")
