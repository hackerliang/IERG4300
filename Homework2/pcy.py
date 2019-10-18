"""pcy.py
This file implements the PCY algorithm to find the frequent item pair.
A part of Homework #2, IERG4300, CUHK, S1 2019-2020.
"""

import glob
import json
import itertools as it
from operator import itemgetter


def custom_hash(item1, item2):
    return hash(item1 + item2) % 100000


def read_baskets(path, threshold):
    """Read baskets from files.
    @:param path to data, str.
    @:param threshold, float.
    @:return baskets, 2D list.
    @:return buckets, dictionary.
    @:return support, int.
    """
    # Format of the file:
    # One line -> one basket (word separated by \t)
    # One line has 0 - 40 words
    baskets = []
    buckets = {}
    for filename in glob.glob(path + '\\*'):
        with open(filename, 'r', encoding='utf8') as f:
            lines = [line.rstrip('\n') for line in f]
            # For each line, divide the words.
            for line in lines:
                words = line.split()
                baskets += [sorted(words)]
                # Construct item pairs.
                pairs = list(it.combinations(words, 2))
                for pair in pairs:
                    # Hash to create index.
                    index = custom_hash(pair[0], pair[1])
                    buckets[index] = 1 if index not in buckets else buckets[index] + 1
    # Convert precentage to count
    support = int(threshold * len(baskets))
    return baskets, buckets, support


def buckets_to_bitmap(buckets, support):
    """Put the buckets to a bit map. Only keep the buckets are frequent.
    @:param hashed buckets. dict.
    @:param minimum support. int.
    @:return bitmap, dict.
    """
    bitmap = []
    for key, value in buckets.items():
        if value < support:
            bitmap += [(key, 0)]
        else:
            bitmap += [(key, 1)]
    return bitmap


