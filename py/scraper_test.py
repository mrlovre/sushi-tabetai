import unittest

from scraper import Scraper
from utility import remove_accent


class TestScraper(unittest.TestCase):
    def test_vrata(self):
        s = Scraper("vrata")
        data = s.etymologies[0]
        self.assertEqual(remove_accent(data["spelling"]), "vrata")
        self.assertEqual(data["gender"], "n\xa0pl")

    def test_macka(self):
        s = Scraper("mačka")
        data = s.etymologies[0]
        self.assertEqual(remove_accent(data["spelling"]), "mačka")


    def test_pas(self):
        s = Scraper("pas")
        data = s.etymologies[0]

    def test_cijev(self):
        s = Scraper("cijev")
        data = s.etymologies[0]

    def test_prijevoz(self):
        s = Scraper("prijevoz")
        data = s.etymologies[0]

    def test_rijeka(self):
        s = Scraper("rijeka")
        data = s.etymologies[0]

    def test_srijeda(self):
        s = Scraper("srijeda")
        data = s.etymologies[0]
