#!/usr/bin/python3
# -*- coding: utf-8 -*-

import textwrap
from functools import lru_cache
from urllib.parse import urljoin

import bs4
import requests

import html2text

from .util import breakline, default_headers, soup_to_abs


class Bubble:

    def __init__(self, api, other, div):
        self.other = other
        self.me = "bg-bubble-me" in div.attrs["class"]
        self.time = div.find("time").attrs["datetime"]
        div.find("time").extract()
        self.text = html2text.html2text(str(div)).strip()
        self.text = breakline.sub(r"\n\n", self.text)


class Thread:

    def __init__(self, api, tr):
        self.api = api
        self.unread = "unread" in tr.attrs.get("class", "")
        a = tr.select("td.mail-subject a")[0]
        self.url = a.attrs["href"]
        self.id = int(self.url.split("/")[-1])
        self.sender = tr.select("td.sender a")[0].get_text().strip()
        self.subject = a.get_text().strip()
        self.time = tr.find("time").attrs["datetime"]

    @property
    @lru_cache(maxsize=1)
    def key(self):
        return (self.sender, self.subject)

    @property
    @lru_cache(maxsize=1)
    def bubbles(self):
        bbs = []
        s = self.api.get(self.url)
        for div in s.select("div.bubble"):
            bbs.append(Bubble(self.api, self.sender, div))
        return bbs

    @property
    @lru_cache(maxsize=1)
    def answered(self):
        print ("ooooo")
        for b in self.bubbles:
            if b.me:
                return True
        return False

    @property
    @lru_cache(maxsize=1)
    def final(self):
        lst = []
        for b in reversed(self.bubbles):
            if b.me:
                break
            else:
                lst.append(b)
        return list(reversed(lst))

    def reply(self, text):
        text = textwrap.dedent(text).strip()
        s = self.api.get(self.url)
        self.api.submit(s.find("form"), {
            "body": text
        })


class NoLoTiro:

    def __init__(self, email, password):
        self.s = requests.Session()
        self.s.headers = default_headers
        self.root = "https://nolotiro.org/"
        soup = self.get("https://nolotiro.org/es/user/login")
        self.submit(soup.find("form"), {
            "user[email]": email,
            "user[password]": password
        })

    def get(self, url, data=None):
        url = urljoin(self.root, url)
        if data is None:
            r = self.s.get(url)
        else:
            r = self.s.post(url, data=data)
        s = bs4.BeautifulSoup(r.content, "lxml")
        soup_to_abs(s, url)
        return s

    def submit(self, form, data):
        for n in form.findAll("input"):
            name = n.attrs.get("name", None)
            if name and name not in data:
                data[name] = n.attrs.get("value", None)
        self.get(form.attrs["action"], data)

    def threads(self):
        soup = self.get("https://nolotiro.org/es/conversations")
        for tr in soup.select("table.mail-list tbody tr"):
            yield Thread(self, tr)
