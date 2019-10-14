"""SON.py
This file implements the A-Priori algorithm for finding similar item sets.
A part of Homework #2, IERG4300, CUHK, S1 2019-2020.
"""

import glob


def read_baskets(path, threshold):
    """Read baskets from files.
    @param: path to data, str.
    @param: threshold, float.
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
                baskets += [sorted(words)]
    # Convert precentage to count
    freq_count = threshold * len(baskets)
    return baskets, freq_count


def freq_items(baskets, freq_count):
    """Find the individual items appear frequently.
    @param: baskets, 2D list.
    @param: threshold, int.
    @return: frequent individual items with counts, dict.
    """
    items = {}
    # Iterate all items, then count the appearances.
    for basket in baskets:
        for word in basket:
            if word not in items:
                items[word] = 1
            else:
                items[word] += 1
    # Remove non-frequent items.
    freq_items = {}
    for item, count in items.items():
        if count >= freq_count:
            freq_items[item] = count
    return freq_items


def freq_pairs(baskets, freq_items, freq_count):
    """Find the frequent item pairs.
    @param: baskets, 2D list.
    @param: frequent individual items with counts, dict.
    @param: threshold, int.
    @return: frequent pairs with counts, dict.
    """
    pass


if __name__ == '__main__':
    baskets, freq_count = read_baskets('D:\\Datasets\\shakespeare_basket\\test')
    # freqitems = freq_items(baskets, 1)
    # freqpairs = freq_pairs(baskets, freq_items, 1)
