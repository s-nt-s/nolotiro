import re
from urllib.parse import urljoin
import textwrap
import requests


default_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Expires": "Thu, 01 Jan 1970 00:00:00 GMT",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    "X-Requested-With": "XMLHttpRequest",
}

breakline = re.compile(r"[\n]{3,}")
sp = re.compile(r"\s+")

def rel_to_abs(node, attr, root):
    if attr in node.attrs:
        node.attrs[attr] = urljoin(root, node.attrs[attr])


def soup_to_abs(soup, root):
    for a in soup.findAll("a"):
        rel_to_abs(a, "href", root)
    for a in soup.findAll(["img", "frame", "iframe"]):
        rel_to_abs(a, "src", root)
    for a in soup.findAll("from"):
        rel_to_abs(a, "action", root)

def cfg(path):
    with open(path, 'r') as f:
        l = f.readline().strip()
        return sp.split(l)

def read(path):
    with open(path, 'r') as f:
        text = f.read()
        text = textwrap.dedent(text).strip()
        return text

def read_tuples(path):
    txt = read(path)
    tps = [tuple(l.strip().split("\t")) for l in txt.split("\n") if len(l.strip())]
    return tps
