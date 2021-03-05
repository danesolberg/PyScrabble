import os
import sys
from gaddag.gaddag import GADDAG
from gaddag.cgaddag import cgaddag


#  PyGADDAG monkey patch for python < 3.7
if sys.version_info < (3, 7):
    def add_word(self, word):
        """
        Add a word to the GADDAG.

        Args:
            word: A word to be added to the GADDAG.
        """
        word = word.lower()

        if not word.isalpha():
            raise ValueError("Invalid character in word '{}'".format(word))

        word = word.encode(encoding="ascii")
        result = cgaddag.gdg_add_word(self.gdg, word)
        if result == 1:
            raise ValueError("Invalid character in word '{}'".format(word))
        elif result == 2:
            raise MemoryError("Out of memory, GADDAG is in an undefined state")

    GADDAG.add_word = add_word


def load_gdg(dic_path):
    with open(dic_path, 'r') as dic:
        for line in dic:
            gdg.add_word(line.strip('\n'))


DICTIONARY = os.path.dirname(os.path.abspath(__file__)) + '/../../dictionary.txt'


gdg = GADDAG()
load_gdg(DICTIONARY)
