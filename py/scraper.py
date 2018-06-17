import re
from collections import defaultdict
from urllib.parse import quote
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup


class Scraper:
    BASE_URL = "https://en.wiktionary.org/wiki/{word}"

    def __init__(self, word):
        self.word = word
        self.bs = self._get_bs()
        raw_etymologies = self._get_etymologies()
        self.etymologies = [self._process_etymology(etymology) for etymology in raw_etymologies]
        self.n_etymologies = len(self.etymologies)

    @staticmethod
    def _strip(text):
        if text.endswith("[edit]"):
            text = text[:-len("[edit]")]

        return text

    def _get_bs(self):
        with urlopen(self.BASE_URL.format(word=quote(self.word))) as response:
            html_data = response.read().decode("utf8")

        return BeautifulSoup(html_data, "lxml")

    def _get_etymologies(self):
        root = self.bs.find(id="Serbo-Croatian").parent
        etymologies = []
        current = root.find_next_sibling()
        key = "Etymology"
        etymology = defaultdict(list)
        while current is not None and current.name != "hr":
            text = Scraper._strip(current.text)
            if text.startswith("Etymology"):
                if not etymology:
                    etymology = defaultdict(list)

                etymologies.append(etymology)
                key = "Etymology"
            elif re.match(r"h[1-6]", current.name):
                key = text
            else:
                etymology[key].append(current)

            current = current.find_next_sibling()

        if not etymologies:
            etymologies.append(etymology)

        return etymologies

    def _get_noun_data(self, etymology):
        data = {}
        noun = etymology["Noun"]
        data["spelling"] = noun[0].find("strong", class_="Latn headword").text
        data["gender"] = noun[0].find("span", class_="gender").text
        data["meanings"] = [child.text.splitlines()[0] for child in noun[1].children if child.name == "li"]
        declension_info = etymology["Declension"][0].contents[3].find("table")
        data["declension"] = pd.read_html(str(declension_info), header=0, index_col=0)[0]

        if "Alternative forms" in etymology.keys():
            data["alternative_forms"] = [child.text.splitlines()[0] for child in etymology["Alternative forms"][0].children if child.name == "li"]

        return data

    def _process_etymology(self, etymology):
        if "Noun" in etymology.keys():
            return self._get_noun_data(etymology)

        return None
