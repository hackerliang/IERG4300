"""SON.py
This file implements the A-Priori algorithm for finding similar item sets.
A part of Homework #2, IERG4300, CUHK, S1 2019-2020.
"""

import glob
import json
from operator import itemgetter


def read_baskets(path, threshold):
    """Read baskets from files.
    @param: path to data, str.
    @param: threshold, float.
    @return: baskets, 2D list.
    @return: freq_count, int.
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
    freq_count = int(threshold * len(baskets))
    return baskets, freq_count


def freq_items(baskets, freq_count):
    """Find the individual items appear frequently.
    @param: baskets, 2D list.
    @param: min count for a frequent item, int.
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
    @param: the baskets, 2D list
    @param: frequent individual items with counts, dict.
    @param: min count for a frequent pair, int.
    @return: frequent pairs with counts, dict.
    """
    # Construct pairs from frequent items.
    # If a pair is frequent, both of the members are frequent.
    pairs = {}
    items = list(freq_items.keys())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            pairs[(items[i], items[j])] = 0
    # Find and count the pairs in each basket
    for basket in baskets:
        for i in range(len(basket)):
            for j in range(i + 1, len(basket)):
                if (basket[i], basket[j]) in pairs:
                    pairs[(basket[i], basket[j])] += 1
                elif (basket[j], basket[i]) in pairs:
                    pairs[(basket[j], basket[i])] += 1
                else:
                    continue
    # Remove non-frequent pairs.
    freq_pairs = {}
    for pair, count in pairs.items():
        if count >= freq_count:
            freq_pairs[pair] = count
    # Sort the dictionary.
    freq_pairs = sorted(freq_pairs.items(), key=itemgetter(1))
    return freq_pairs


if __name__ == '__main__':
    baskets, freq_count = read_baskets('D:\\Datasets\\shakespeare_basket\\', 0.005)
    freqitems = freq_items(baskets, 2)
    freqpairs = freq_pairs(baskets, freqitems, 2)
    # Save to file
    json.dump(freqpairs, open('freq_pairs.json', 'w'), indent=2)
