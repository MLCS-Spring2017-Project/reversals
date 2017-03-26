"""
District court to circuit court linker class
"""

from bs4 import BeautifulSoup


class DCTCCLinker:
    def __init__(self):
        return

    """
    Dic contains following keys
    """
    def link(self, case_name, txt):
        soup = BeautifulSoup(txt, "html.parser")
        h2 = soup.find("h2")

        if h2:
            h2 = h2.text.strip().lower()
            return case_name in h2
        else:
            return False
