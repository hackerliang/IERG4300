"""APriori.py
This file implements the A-Priori algorithm for finding similar item sets.
A part of Homework #2, IERG4300, CUHK, S1 2019-2020.
"""


def read_baskets(path):
    """Read baskets from files.
    @param: path to data, str.
    @return: baskets, 2D list.
    """
    pass


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
    baskets = read_baskets('D:\\Datasets\\shakespeare_basket')
    freq_items = freq_items(baskets, 1)
    freq_pairs = freq_pairs(baskets, freq_items, 1)
