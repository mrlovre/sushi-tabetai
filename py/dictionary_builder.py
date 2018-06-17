import sys

from scraper import Scraper
from utility import minipage, remove_accent


def process_etymology(etym, header=False):
    if header:
        print(rf"\section{{\underline{{{etym['spelling']} ({etym['gender']})}}}}")
    else:
        print(rf"\section{{{etym['spelling']} ({etym['gender']})}}")

    if "alternative_forms" in etym.keys():
        print(r"\subsection*{Alternative forms}")
        print(r"\begin{enumerate}")

        for form in etym["alternative_forms"]:
            print(rf"\item {form}")

        print(r"\end{enumerate}")

    print(r"\subsection*{Meanings}")
    print(r"\begin{enumerate}")

    for meaning in etym["meanings"]:
        print(rf"\item {meaning}")

    print(r"\end{enumerate}")
    print(r"\subsection*{Declension pattern}")
    declension = etym["declension"]
    print(declension.to_latex(bold_rows=True, column_format="r" + "l" * len(declension.columns)))


def print(*args, **kwargs):
    from builtins import print as _print
    nargs = [remove_accent(arg) if isinstance(arg, str) else arg for arg in args]
    _print(*nargs, **kwargs)


if __name__ == '__main__':
    with open("list_clean") as file:
        text = file.read()
    with open("output/output.tex", "w") as file:
        def write_file(string):
            pass

        sys.stdout = file
        words = text.splitlines()
        header = True
        for word in words:
            print(word, file=sys.stderr)
            if not word:
                # print(r"\pagebreak")
                header = True
                continue

            if word.lstrip().startswith("#"):
                continue

            try:
                scraper = Scraper(word)
                for etymology in scraper.etymologies:
                    with minipage():
                        process_etymology(etymology, header)
            except Exception as e:
                print(e, file=sys.stderr)
                print(rf"\section{{{word}}}")
                print(r"{\# TBD}")

            header = False
