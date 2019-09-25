#!/usr/bin/python3
"""mapper2.py
Input: (user_id_1,user_id_2) \t 1
Output: same as the input

This mapper does nothing. Just pass the input to the reducer.
Let the MapReduce engine to sort the keys automatically.
"""

import fileinput

for line in fileinput.input():
    print(line)