#!/usr/bin/python3
"""partitioner.py
This script defines the secondary sort for the key-value pairs.
The sorting order should be, movie_id -> rating.
For users gave a same rating for a movie, will be sorted together.
Each of the reduce task will aggregate the users.
"""