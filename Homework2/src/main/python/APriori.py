"""APriori.py
This file implements the A-Priori algorithm for finding similar item sets.
A part of Homework #2, IERG4300, CUHK, S1 2019-2020.
"""

import glob

def read_baskets(path):
    """Read baskets from files.
    @param: path to data, str.
    @return: baskets, 2D list.
    """
    # Format of the file:
    # One line -> one basket (word separated by \t)
    # One line has 0 - 40 words
    baskets = []
    for filename in glob.glob(path + '\\*'):
        with open(filename, 'r', encoding='utf8') as f:
            lines = [line.rstrip('\n') for line in f]
            # For each line, divide the words.
            for line in lines:
                words = line.split()
                baskets += [words]
    return baskets



def freq_items(baskets, threshold):
    """Find the individual items appear frequently.
    @param: baskets, 2D list.
    @param: threshold, int.
    @return: frequent individual items with counts, dict.
    """
    pass


def freq_pairs(baskets, freq_items, threshold):
    """Find the frequent item pairs.
    @param: baskets, 2D list.
    @param: frequent individual items with counts, dict.
    @param: threshold, int.
    @return: frequent pairs with counts, dict.
    """
    pass


if __name__ == '__main__':
    baskets = read_baskets('D:\\Datasets\\shakespeare_basket\\test')
    # freq_items = freq_items(baskets, 1)
    # freq_pairs = freq_pairs(baskets, freq_items, 1)
