from unidecode import unidecode


class Minipage:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(r"\filbreak")


minipage = Minipage

DIACRITIC = {"č", "ć", "š", "đ", "ž", "Č", "Ć", "Š", "Đ", "Ž"}


def remove_accent(word: str) -> str:
    pure = unidecode(word)
    return str.join("", [c if c in DIACRITIC else d for c, d in zip(word, pure)])
